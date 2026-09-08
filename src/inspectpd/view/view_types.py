"""Plot for :func:`inspectpd.inspect_types`."""

from __future__ import annotations

import pandas as pd
import plotnine as p9

from inspectpd.view.utils import labelled_bar_chart


def view_types(df: pd.DataFrame) -> p9.ggplot:
    """Bar chart of the number of columns with each dtype."""
    if df.shape[0] == 0:
        raise ValueError("no columns to view")
    return labelled_bar_chart(
        df, x="type", y="cnt", label="cnt", ylab="Number of columns"
    )
