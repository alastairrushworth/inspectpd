"""Summary of feature imbalance in categorical columns."""

from __future__ import annotations

import numpy as np
import pandas as pd

from inspectpd.inspect._common import level_table, select_categorical, validate_frame
from inspectpd.inspect_object.inspect_object import InspectFrame


def inspect_imb(df: pd.DataFrame) -> InspectFrame:
    """Summarise the most common level in each categorical column.

    Columns with ``category``, ``object``, ``string``/``str``, ``bool`` or
    ``boolean`` dtype are included. Missing values are ignored, so ``pcnt``
    is relative to the non-missing rows of each column. A column that is
    entirely missing gets a missing ``value``, ``cnt`` 0 and ``pcnt`` ``NaN``.

    Parameters
    ----------
    df : pandas.DataFrame
        The data frame to summarise.

    Returns
    -------
    InspectFrame
        One row per categorical column, sorted by ``pcnt`` descending, with
        columns:

        ``col_name`` : object
            Name of the column in ``df``.
        ``value`` : object
            The most common level in the column.
        ``cnt`` : int64
            Number of occurrences of that level.
        ``pcnt`` : float64
            Percentage of non-missing rows occupied by that level.
    """
    df = validate_frame(df)
    df_cat = select_categorical(df)
    levels = [level_table(df_cat[col], dropna=True) for col in df_cat.columns]
    out = pd.DataFrame(
        {
            "col_name": df_cat.columns.to_numpy(dtype=object),
            "value": [lv["value"].iloc[0] if len(lv) else None for lv in levels],
            "cnt": [int(lv["cnt"].iloc[0]) if len(lv) else 0 for lv in levels],
            "pcnt": [lv["pcnt"].iloc[0] if len(lv) else np.nan for lv in levels],
        }
    )
    out = out.sort_values("pcnt", ascending=False, kind="stable").reset_index(drop=True)
    return InspectFrame(out, inspect_type="inspect_imb")
