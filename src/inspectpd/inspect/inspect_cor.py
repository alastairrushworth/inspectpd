"""Tidy pairwise correlations between numeric columns."""

from __future__ import annotations

from collections.abc import Hashable

import numpy as np
import pandas as pd

from inspectpd.inspect._common import select_numeric, validate_frame
from inspectpd.inspect_object.inspect_object import InspectFrame

_METHODS = ("pearson", "kendall", "spearman")
_COLUMNS = ["col_1", "col_2", "corr", "p_value", "lower", "upper", "pcnt_nna"]


def inspect_cor(
    df: pd.DataFrame,
    method: str = "pearson",
    alpha: float = 0.05,
    with_col: Hashable | None = None,
) -> InspectFrame:
    """Compute tidy correlation coefficients between numeric columns.

    Correlations use pairwise complete observations. Confidence intervals
    and p-values come from the Fisher z transformation, with the standard
    error appropriate to ``method`` (Pearson: ``1/sqrt(n-3)``; Spearman:
    ``sqrt((1 + r^2/2)/(n-3))``; Kendall: ``sqrt(0.437/(n-4))``). Pairs with
    too few complete observations for that standard error get ``NaN``
    p-values and intervals.

    Parameters
    ----------
    df : pandas.DataFrame
        The data frame to summarise.
    method : {"pearson", "kendall", "spearman"}, default "pearson"
        Correlation coefficient to compute.
    alpha : float, default 0.05
        Significance level for the confidence intervals, so the default gives
        95% intervals. Also used by :meth:`InspectFrame.view` to colour pairs.
    with_col : hashable, optional
        Restrict the output to correlations between this numeric column and
        every other numeric column. Uses ``DataFrame.corrwith`` instead of
        the full matrix, which is faster on wide frames.

    Returns
    -------
    InspectFrame
        One row per pair of numeric columns, sorted by absolute correlation
        descending, with columns:

        ``col_1``, ``col_2`` : object
            Names of the two columns.
        ``corr`` : float64
            The correlation coefficient. Access it with ``result["corr"]``,
            because ``result.corr`` is the pandas method.
        ``p_value`` : float64
            Two-sided p-value for the null hypothesis of zero correlation.
        ``lower``, ``upper`` : float64
            Confidence interval for the correlation.
        ``pcnt_nna`` : float64
            Percentage of rows where both columns are non-missing.

    Raises
    ------
    ValueError
        If ``method`` is unknown, ``alpha`` is outside ``(0, 1)``, or
        ``with_col`` is not a numeric column of ``df``.
    """
    df = validate_frame(df)
    if method not in _METHODS:
        raise ValueError(f"method must be one of {_METHODS}, got {method!r}")
    if not 0 < alpha < 1:
        raise ValueError(f"alpha must be strictly between 0 and 1, got {alpha!r}")
    df_num = select_numeric(df)
    nrow = df.shape[0]
    params = {"method": method, "alpha": alpha, "with_col": with_col}

    if with_col is None:
        cor = df_num.corr(method=method)
        i, j = np.triu_indices(cor.shape[0], k=1)
        out = pd.DataFrame(
            {
                "col_1": cor.index.to_numpy(dtype=object)[i],
                "col_2": cor.columns.to_numpy(dtype=object)[j],
                "corr": cor.to_numpy()[i, j],
            }
        )
    else:
        if with_col not in df_num.columns:
            raise ValueError(
                f"with_col={with_col!r} is not a numeric column of the data frame"
            )
        others = df_num.drop(columns=[with_col])
        cor = others.corrwith(df_num[with_col], method=method)
        out = pd.DataFrame(
            {
                "col_1": cor.index.to_numpy(dtype=object),
                "col_2": with_col,
                "corr": cor.to_numpy(dtype="float64"),
            }
        )
    if out.empty:
        return InspectFrame(
            pd.DataFrame(columns=_COLUMNS),
            inspect_type="inspect_cor",
            inspect_params=params,
        )

    # number of pairwise complete observations for each pair
    present = df_num.notna().astype("int64")
    nna = present.T.dot(present)
    out["n"] = [nna.at[a, b] for a, b in zip(out["col_1"], out["col_2"], strict=True)]
    out["pcnt_nna"] = 100 * out["n"] / nrow if nrow else np.nan

    # Fisher z based p-values and confidence intervals
    from scipy import stats  # deferred: scipy.stats is slow to import

    r = out["corr"].to_numpy(dtype="float64")
    n = out["n"].to_numpy(dtype="float64")
    with np.errstate(all="ignore"):
        se = _fisher_se(r, n, method)
        z = np.arctanh(r)
        zcrit = stats.norm.ppf(1 - alpha / 2)
        out["p_value"] = 2 * stats.norm.sf(np.abs(z) / se)
        out["lower"] = np.tanh(z - zcrit * se)
        out["upper"] = np.tanh(z + zcrit * se)

    out = (
        out.assign(_abs=out["corr"].abs())
        .sort_values("_abs", ascending=False, kind="stable", na_position="last")
        .reset_index(drop=True)[_COLUMNS]
    )
    return InspectFrame(out, inspect_type="inspect_cor", inspect_params=params)


def _fisher_se(r: np.ndarray, n: np.ndarray, method: str) -> np.ndarray:
    """Return the standard error of the Fisher z transformed coefficient."""
    if method == "pearson":
        se = 1 / np.sqrt(n - 3)
    elif method == "spearman":
        se = np.sqrt((1 + r**2 / 2) / (n - 3))
    else:  # kendall
        se = np.sqrt(0.437 / (n - 4))
    return np.where(np.isfinite(se), se, np.nan)
