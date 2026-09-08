"""Summary of memory usage by column."""

from __future__ import annotations

import pandas as pd

from inspectpd.inspect._common import validate_frame
from inspectpd.inspect_object.inspect_object import InspectFrame

_UNITS = ["B", "KiB", "MiB", "GiB", "TiB", "PiB", "EiB", "ZiB", "YiB"]


def inspect_mem(df: pd.DataFrame) -> InspectFrame:
    """Summarise the memory used by each column of a DataFrame.

    Parameters
    ----------
    df : pandas.DataFrame
        The data frame to summarise.

    Returns
    -------
    InspectFrame
        One row per column, sorted by ``bytes`` descending, with columns:

        ``col_name`` : object
            Name of the column in ``df``.
        ``bytes`` : int64
            Memory used by the column in bytes (``deep=True`` accounting).
        ``size`` : object
            The same figure as a display string in binary units (KiB, MiB
            and so on). Access it with ``result["size"]``, because
            ``result.size`` is the pandas element count.
        ``pcnt`` : float64
            Percentage of the frame's total memory used by the column.
    """
    df = validate_frame(df)
    usage = df.memory_usage(index=False, deep=True)
    total = usage.sum()
    out = pd.DataFrame(
        {
            "col_name": df.columns.to_numpy(dtype=object),
            "bytes": usage.to_numpy(),
        }
    )
    out["size"] = [format_size(int(b)) for b in out["bytes"]]
    out["pcnt"] = 100 * out["bytes"] / total if total else float("nan")
    out = out.sort_values("bytes", ascending=False, kind="stable").reset_index(
        drop=True
    )
    return InspectFrame(out, inspect_type="inspect_mem")


def format_size(num_bytes: float) -> str:
    """Format a byte count as a short string in binary units, e.g. ``"1.50 KiB"``."""
    size = float(num_bytes)
    for unit in _UNITS[:-1]:
        if size < 1024.0:
            return f"{size:3.0f} {unit}" if unit == "B" else f"{size:3.2f} {unit}"
        size /= 1024.0
    return f"{size:3.2f} {_UNITS[-1]}"
