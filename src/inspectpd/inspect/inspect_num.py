"""Summary of numeric columns."""

from __future__ import annotations

import numpy as np
import pandas as pd

from inspectpd.inspect._common import object_column, select_numeric, validate_frame
from inspectpd.inspect_object.inspect_object import InspectFrame

_HIST_BINS = 10


def inspect_num(df: pd.DataFrame) -> InspectFrame:
    """Summarise the numeric columns of a DataFrame.

    Every numeric dtype is included (integer, float, and the nullable
    ``Int64`` / ``Float64`` types); boolean columns are not.

    Parameters
    ----------
    df : pandas.DataFrame
        The data frame to summarise.

    Returns
    -------
    InspectFrame
        One row per numeric column, in column order, with columns:

        ``col_name`` : object
            Name of the column in ``df``.
        ``min``, ``q1``, ``median``, ``mean``, ``q3``, ``max``, ``sd`` : float64
            Minimum, lower quartile, median, mean, upper quartile, maximum
            and standard deviation. Access these with ``result["min"]`` and
            so on, because ``result.min`` is the pandas method.
        ``pcnt_na`` : float64
            Percentage of the column that is missing.
        ``hist`` : object
            A frame per column with ``value`` (an interval) and ``prop``
            (the proportion of finite values falling in it) for ten equal
            width bins. Access it with ``result["hist"]``.
    """
    df = validate_frame(df)
    df_num = select_numeric(df)
    out = pd.DataFrame({"col_name": df_num.columns.to_numpy(dtype=object)})
    # infinite values make the mean and sd undefined; numpy would warn about
    # the resulting inf - inf, but NaN in the output already says it all
    with np.errstate(invalid="ignore"):
        out["min"] = df_num.min().to_numpy()
        out["q1"] = df_num.quantile(0.25).to_numpy()
        out["median"] = df_num.median().to_numpy()
        out["mean"] = df_num.mean().to_numpy()
        out["q3"] = df_num.quantile(0.75).to_numpy()
        out["max"] = df_num.max().to_numpy()
        out["sd"] = df_num.std().to_numpy()
    out["pcnt_na"] = 100 * df_num.isna().mean().to_numpy(dtype="float64")
    out["hist"] = object_column([_histogram(df_num[col]) for col in df_num.columns])
    return InspectFrame(out, inspect_type="inspect_num")


def _histogram(series: pd.Series) -> pd.DataFrame:
    """Relative frequency of the finite values of ``series`` in equal-width bins."""
    finite = series[np.isfinite(series)]
    if finite.empty:
        return pd.DataFrame({"value": pd.IntervalIndex([]), "prop": []})
    props = pd.cut(finite, bins=_HIST_BINS).value_counts(normalize=True, sort=False)
    # Store the bins as a plain interval column rather than the categorical
    # index value_counts returns: categorical interval columns get hashed by
    # pandas during concat and dtype inference, which is slow and, with some
    # numpy builds, emits spurious RuntimeWarnings.
    bins = props.index.categories.take(props.index.codes)
    return pd.DataFrame({"value": bins, "prop": props.to_numpy()})
