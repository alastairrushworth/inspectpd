"""Summary of missing values by column."""

from __future__ import annotations

import pandas as pd

from inspectpd.inspect._common import validate_frame
from inspectpd.inspect_object.inspect_object import InspectFrame


def inspect_na(df: pd.DataFrame) -> InspectFrame:
    """Summarise the rate of missingness in each column of a DataFrame.

    Parameters
    ----------
    df : pandas.DataFrame
        The data frame to summarise.

    Returns
    -------
    InspectFrame
        One row per column, sorted by ``pcnt`` descending, with columns:

        ``col_name`` : object
            Name of the column in ``df``.
        ``cnt`` : int64
            Number of missing values in the column.
        ``pcnt`` : float64
            Percentage of rows in the column that are missing.
    """
    df = validate_frame(df)
    null = df.isna()
    out = pd.DataFrame(
        {
            "col_name": df.columns.to_numpy(dtype=object),
            "cnt": null.sum().to_numpy(),
            "pcnt": 100 * null.mean().to_numpy(dtype="float64"),
        }
    )
    out = out.sort_values("pcnt", ascending=False, kind="stable").reset_index(drop=True)
    return InspectFrame(out, inspect_type="inspect_na")
