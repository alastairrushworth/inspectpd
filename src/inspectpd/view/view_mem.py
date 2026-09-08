"""Plot for :func:`inspectpd.inspect_mem`."""

from __future__ import annotations

import pandas as pd
import plotnine as p9

from inspectpd.view.utils import labelled_bar_chart


def view_mem(df: pd.DataFrame) -> p9.ggplot:
    """Bar chart of the share of total memory used by each column."""
    if df.shape[0] == 0:
        raise ValueError("no columns to view")
    return labelled_bar_chart(
        df, x="col_name", y="pcnt", label="size", ylab="% of total size"
    )
