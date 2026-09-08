"""Summary of the levels found in categorical columns."""

from __future__ import annotations

import pandas as pd

from inspectpd.inspect._common import (
    level_table,
    object_column,
    select_categorical,
    validate_frame,
)
from inspectpd.inspect_object.inspect_object import InspectFrame


def inspect_cat(df: pd.DataFrame) -> InspectFrame:
    """Summarise the levels in the categorical columns of a DataFrame.

    Columns with ``category``, ``object``, ``string``/``str``, ``bool`` or
    ``boolean`` dtype are included. Missing values are counted as a level.

    Parameters
    ----------
    df : pandas.DataFrame
        The data frame to summarise.

    Returns
    -------
    InspectFrame
        One row per categorical column, sorted by column name, with columns:

        ``col_name`` : object
            Name of the column in ``df``.
        ``cnt`` : int64
            Number of unique levels (including missing, if present).
        ``common`` : object
            The most common level.
        ``common_pcnt`` : float64
            Percentage of rows occupied by the most common level.
        ``levels`` : object
            A frame per column with ``value``, ``pcnt`` and ``cnt`` for every
            level, most common first. Access it with ``result["levels"]``.
    """
    df = validate_frame(df)
    df_cat = select_categorical(df)
    levels = [level_table(df_cat[col], dropna=False) for col in df_cat.columns]
    out = pd.DataFrame(
        {
            "col_name": df_cat.columns.to_numpy(dtype=object),
            "cnt": [len(lv) for lv in levels],
            "common": [lv["value"].iloc[0] if len(lv) else None for lv in levels],
            "common_pcnt": [
                lv["pcnt"].iloc[0] if len(lv) else float("nan") for lv in levels
            ],
            "levels": object_column(levels),
        }
    )
    out = out.sort_values("col_name", kind="stable").reset_index(drop=True)
    return InspectFrame(out, inspect_type="inspect_cat")
