"""Plot for :func:`inspectpd.inspect_cor`."""

from __future__ import annotations

import numpy as np
import pandas as pd
import plotnine as p9

_COLOURS = {"yes": "#3b5bdb", "no": "#abaeb3"}


def view_cor(df: pd.DataFrame, max_pairs: int | None = 20) -> p9.ggplot:
    """Confidence-interval bars for the strongest correlations.

    Parameters
    ----------
    df : InspectFrame
        Output of :func:`inspectpd.inspect_cor`.
    max_pairs : int or None, default 20
        Draw at most this many pairs, strongest first. ``None`` draws all.
    """
    if df.shape[0] == 0:
        raise ValueError("no numeric column pairs to view")
    data = df[df["corr"].notna()]
    if data.empty:
        raise ValueError("all correlations are NaN")
    if max_pairs is not None:
        data = data.iloc[:max_pairs]

    params = getattr(df, "inspect_params", None) or {}
    alpha = params.get("alpha", 0.05)

    pairs = [f"{a} & {b}" for a, b in zip(data["col_1"], data["col_2"], strict=True)]
    data = pd.DataFrame(
        {
            # reversed so the strongest pair sits at the top after coord_flip
            "pair": pd.Categorical(pairs, categories=pairs[::-1], ordered=True),
            "corr": data["corr"].to_numpy(),
            # pairs without an interval (too few observations) draw as a line
            "lower": data["lower"].fillna(data["corr"]).to_numpy(),
            "upper": data["upper"].fillna(data["corr"]).to_numpy(),
            "significant": np.where(data["p_value"] < alpha, "yes", "no"),
        }
    )
    return (
        p9.ggplot(
            data,
            p9.aes(x="pair", y="corr", ymin="lower", ymax="upper", fill="significant"),
        )
        + p9.geom_hline(yintercept=0, linetype="dashed", color="#c2c6cc")
        + p9.geom_crossbar(width=0.8, alpha=0.4, color="black")
        + p9.scale_fill_manual(values=_COLOURS, limits=["yes", "no"], drop=False)
        + p9.coord_flip()
        + p9.labs(x="", y="Correlation", fill=f"p < {alpha:g}")
    )
