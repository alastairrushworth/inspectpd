"""Plotting helpers shared by the ``view_*`` functions."""

from __future__ import annotations

import numpy as np
import pandas as pd
import plotnine as p9


def text_sizer(nvars: int) -> float:
    """Shrink label text as the number of bars grows."""
    text_size = 12 - ((nvars + 1) / 8)
    return float(min(12, max(0, text_size)))


def labelled_bar_chart(
    data: pd.DataFrame, *, x: str, y: str, label: str, ylab: str
) -> p9.ggplot:
    """Draw one bar per row of ``data`` with a text label on each bar.

    Bars keep the row order of ``data``. Labels for tall bars (more than 30%
    of the tallest) are drawn in white inside the bar; labels for short bars
    are drawn in grey just above it.

    Parameters
    ----------
    data : pandas.DataFrame
        One row per bar.
    x : str
        Column giving the bar names; converted to strings.
    y : str
        Numeric column giving the bar heights.
    label : str
        Column with the text to print on each bar.
    ylab : str
        Y axis title.
    """
    x_labels = [str(v) for v in data[x]]
    frame = pd.DataFrame(
        {
            "x": pd.Categorical(x_labels, categories=x_labels, ordered=True),
            "y": data[y].to_numpy(dtype="float64"),
            "label": [str(v) for v in data[label]],
        }
    )
    top = np.nanmax(frame["y"].to_numpy()) if frame["y"].notna().any() else 0.0
    frame["y_inside"] = frame["y"] - top / 70
    frame["y_above"] = frame["y"] + top / 70
    text_size = text_sizer(frame.shape[0])

    plot = (
        p9.ggplot(frame, p9.aes(x="x", y="y", fill="x"))
        + p9.geom_col()
        + p9.guides(fill="none")
        + p9.ylab(ylab)
        + p9.xlab("")
        + p9.theme(axis_text_x=p9.element_text(rotation=45, hjust=1))
    )
    tall = frame[frame["y"] > 0.3 * top]
    short = frame[~(frame["y"] > 0.3 * top)]
    if not tall.empty:
        plot = plot + p9.geom_text(
            p9.aes(x="x", y="y_inside", label="label"),
            data=tall,
            inherit_aes=False,
            color="white",
            angle=90,
            va="top",
            ha="center",
            size=text_size,
        )
    if not short.empty:
        plot = plot + p9.geom_text(
            p9.aes(x="x", y="y_above", label="label"),
            data=short,
            inherit_aes=False,
            color="gray",
            angle=90,
            va="bottom",
            ha="center",
            size=text_size,
        )
    return plot
