"""Helpers shared by the ``inspect_*`` summary functions."""

from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd

# dtypes treated as categorical by inspect_cat / inspect_imb. Both the
# pandas 3 default ``str`` dtype and the nullable ``string`` dtype are matched
# by "string"; passing it explicitly avoids the pandas 3 deprecation path that
# folds ``str`` columns into "object".
CATEGORICAL_DTYPES = ["category", "object", "string", "bool", "boolean"]


def validate_frame(df: Any) -> pd.DataFrame:
    """Check that ``df`` is a DataFrame with unique column names.

    Raises
    ------
    TypeError
        If ``df`` is not a :class:`pandas.DataFrame`.
    ValueError
        If ``df`` has duplicate column names.
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError(
            f"expected a pandas DataFrame, got {type(df).__name__}; "
            "for a Series use series.to_frame() first"
        )
    if not df.columns.is_unique:
        dupes = df.columns[df.columns.duplicated()].unique().tolist()
        raise ValueError(f"column names must be unique; duplicated: {dupes}")
    return df


def select_categorical(df: pd.DataFrame) -> pd.DataFrame:
    """Return the categorical, string, object and boolean columns of ``df``."""
    return df.select_dtypes(include=CATEGORICAL_DTYPES)


def select_numeric(df: pd.DataFrame) -> pd.DataFrame:
    """Return the numeric columns of ``df`` as float64.

    Casting up front means integer, float32 and nullable (``Int64`` /
    ``Float64``) columns are all handled the same way downstream, with
    missing values represented as ``NaN``.
    """
    return df.select_dtypes(include="number").astype("float64")


def object_column(items: list[Any]) -> np.ndarray:
    """Pack ``items`` into a 1-d object array, one element per item.

    Use this to store frames or lists inside a column. Handing pandas a plain
    list instead makes it call ``__array__`` on every element to work out a
    dtype, which for a frame means materialising ``.values`` and, on some
    platforms, spurious numpy warnings.
    """
    out = np.empty(len(items), dtype=object)
    for i, item in enumerate(items):
        out[i] = item
    return out


def level_table(series: pd.Series, *, dropna: bool) -> pd.DataFrame:
    """Tabulate the levels of ``series``.

    Returns a frame with columns ``value``, ``pcnt`` and ``cnt`` sorted by
    frequency (most common first) with a fresh 0..n-1 index. ``pcnt`` is
    relative to the rows that were counted, so with ``dropna=True`` missing
    values are excluded from the denominator.
    """
    counts = series.value_counts(dropna=dropna)
    table = pd.DataFrame(
        {
            "value": counts.index.to_numpy(dtype=object),
            "cnt": counts.to_numpy(),
        }
    )
    total = table["cnt"].sum()
    table["pcnt"] = 100 * table["cnt"] / total if total else np.nan
    table = table.sort_values("pcnt", ascending=False, kind="stable")
    return table[["value", "pcnt", "cnt"]].reset_index(drop=True)
