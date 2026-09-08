"""Plot for :func:`inspectpd.inspect_na`."""

from __future__ import annotations

import pandas as pd
import plotnine as p9

from inspectpd.view.utils import labelled_bar_chart


def view_na(df: pd.DataFrame) -> p9.ggplot:
    """Bar chart of the percentage of missing values per column."""
    if df.shape[0] == 0:
        raise ValueError("no columns to view")
    data = df.assign(pcnt_print=df["pcnt"].round(1))
    return labelled_bar_chart(
        data, x="col_name", y="pcnt", label="pcnt_print", ylab="% of values missing"
    )
