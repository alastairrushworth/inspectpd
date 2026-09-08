"""Summary of column dtypes."""

from __future__ import annotations

import pandas as pd

from inspectpd.inspect._common import validate_frame
from inspectpd.inspect_object.inspect_object import InspectFrame


def inspect_types(df: pd.DataFrame) -> InspectFrame:
    """Summarise the column dtypes of a DataFrame.

    Parameters
    ----------
    df : pandas.DataFrame
        The data frame to summarise.

    Returns
    -------
    InspectFrame
        One row per distinct dtype, sorted by ``cnt`` descending, with
        columns:

        ``type`` : object
            The dtype as a string, for example ``"float64"`` or ``"str"``.
        ``cnt`` : int64
            Number of columns with that dtype.
        ``pcnt`` : float64
            Percentage of all columns with that dtype.
        ``col_name`` : object
            List of the column names with that dtype.
    """
    df = validate_frame(df)
    types = pd.DataFrame(
        {
            "col_name": df.columns.to_numpy(dtype=object),
            "type": [str(dtype) for dtype in df.dtypes],
        }
    )
    grouped = types.groupby("type", sort=False)["col_name"].agg(list)
    out = pd.DataFrame(
        {
            "type": grouped.index.to_numpy(dtype=object),
            "cnt": [len(cols) for cols in grouped],
            "col_name": grouped.to_list(),
        }
    )
    ncols = df.shape[1]
    out["pcnt"] = 100 * out["cnt"] / ncols if ncols else float("nan")
    out = out[["type", "cnt", "pcnt", "col_name"]]
    out = out.sort_values("cnt", ascending=False, kind="stable").reset_index(drop=True)
    return InspectFrame(out, inspect_type="inspect_types")
