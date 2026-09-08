"""Plot for :func:`inspectpd.inspect_imb`."""

from __future__ import annotations

import pandas as pd
import plotnine as p9

from inspectpd.view.utils import labelled_bar_chart


def view_imb(df: pd.DataFrame) -> p9.ggplot:
    """Bar chart of the share taken by the most common level of each column."""
    if df.shape[0] == 0:
        raise ValueError("no categorical columns to view")
    return labelled_bar_chart(
        df, x="col_name", y="pcnt", label="value", ylab="% of values"
    )
