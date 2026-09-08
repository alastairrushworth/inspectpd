"""Plot for :func:`inspectpd.inspect_num`."""

from __future__ import annotations

import pandas as pd
import plotnine as p9


def view_num(df: pd.DataFrame) -> p9.ggplot:
    """Faceted histograms of every numeric column."""
    if df.shape[0] == 0:
        raise ValueError("no numeric columns to view")
    # copy each histogram so the caller's summary is left untouched
    tables = [
        hist.assign(groups=str(name))
        for name, hist in zip(df["col_name"], df["hist"], strict=True)
        if not hist.empty
    ]
    if not tables:
        raise ValueError("no numeric columns with finite values to view")
    data = pd.concat(tables, ignore_index=True)
    data["value"] = data["value"].astype(str)
    return (
        p9.ggplot(data, p9.aes(x="value", y="prop", group="groups"))
        + p9.geom_col()
        + p9.ylab("Proportion")
        + p9.xlab("")
        + p9.theme(axis_text_x=p9.element_text(rotation=45, hjust=1))
        + p9.facet_wrap("groups", ncol=3, scales="free")
    )
