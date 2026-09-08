"""Plot for :func:`inspectpd.inspect_cat`."""

from __future__ import annotations

import pandas as pd
import plotnine as p9

_NA_LABEL = "nan"
_HIGH_CARD_LABEL = "High cardinality"
_MIN_LABEL_PCNT = 15


def view_cat(df: pd.DataFrame, high_cardinality: int = 0) -> p9.ggplot:
    """Stacked bars showing the relative frequency of every level per column.

    Parameters
    ----------
    df : InspectFrame
        Output of :func:`inspectpd.inspect_cat`.
    high_cardinality : int, default 0
        Pool levels that occur this many times or fewer into a single block.
        Useful when a column has many unique or near-unique values.
    """
    if df.shape[0] == 0:
        raise ValueError("no categorical columns to view")

    tables = []
    for col_name, levels in zip(df["col_name"], df["levels"], strict=True):
        table = _put_nan_at_top(levels)
        if high_cardinality > 0:
            table = _merge_high_cardinality(table, high_cardinality)
        table = table.reset_index(drop=True)
        table["feature"] = str(col_name)
        # alpha shading fades along the bar from the most to the least common
        alpha = (100 - table["pcnt"].cumsum()) / 100
        span = alpha.max() - alpha.min()
        table["alpha"] = 100 * (alpha - alpha.min()) / span if span else 100.0
        tables.append(table)
    data = pd.concat(tables, ignore_index=True)

    # keep the column order of the summary (reversed, because of coord_flip)
    feature_order = [str(c) for c in df["col_name"]][::-1]
    data["feature"] = pd.Categorical(data["feature"], categories=feature_order)
    data["cum_perc"] = data.groupby("feature", observed=True)["pcnt"].cumsum()
    data["cum_perc"] = data["cum_perc"] - data["pcnt"]

    plot = (
        p9.ggplot(data, p9.aes(x="feature", y="pcnt", fill="feature", alpha="alpha"))
        + p9.geom_col(position="stack", color="black")
        + p9.guides(fill="none", alpha="none")
        + p9.coord_flip()
        + p9.xlab("")
        + p9.ylab("")
        + p9.theme(
            axis_title_y=p9.element_blank(),
            panel_background=p9.element_blank(),
            axis_ticks_minor=p9.element_blank(),
            axis_ticks_major=p9.element_blank(),
            panel_border=p9.element_blank(),
            panel_grid_major=p9.element_blank(),
            axis_title_x=p9.element_blank(),
            axis_text_x=p9.element_blank(),
        )
    )
    # grey block for missing values and purple for pooled high-cardinality levels
    null_items = data[data["value"] == _NA_LABEL]
    if not null_items.empty:
        plot = plot + _colour_subset(null_items, "gray", right=False)
    hc_items = data[data["value"] == _HIGH_CARD_LABEL]
    if high_cardinality > 0 and not hc_items.empty:
        plot = plot + _colour_subset(hc_items, "purple")

    # label the larger blocks
    labels = data.assign(text_pos=data["cum_perc"] + data["pcnt"] / 2)
    labels = labels[labels["pcnt"] > _MIN_LABEL_PCNT].reset_index(drop=True)
    if not labels.empty:
        plot = plot + p9.geom_text(
            data=labels,
            mapping=p9.aes(x="feature", y="text_pos", label="value"),
            inherit_aes=False,
            color="white",
        )
    return plot


def _merge_high_cardinality(table: pd.DataFrame, threshold: int) -> pd.DataFrame:
    """Pool the levels with ``threshold`` or fewer occurrences into one row."""
    is_na = table["value"] == _NA_LABEL
    rare = table[(table["cnt"] <= threshold) & ~is_na]
    keep = table[(table["cnt"] > threshold) | is_na]
    pooled = pd.DataFrame(
        {
            "value": [_HIGH_CARD_LABEL],
            "pcnt": [rare["pcnt"].sum()],
            "cnt": [rare["cnt"].sum()],
        }
    )
    return pd.concat([keep, pooled], ignore_index=True)


def _put_nan_at_top(table: pd.DataFrame) -> pd.DataFrame:
    """Move missing values into a single first row labelled ``"nan"``."""
    is_na = table["value"].isna()
    nan_row = pd.DataFrame(
        {
            "value": [_NA_LABEL],
            "pcnt": [table.loc[is_na, "pcnt"].sum()],
            "cnt": [table.loc[is_na, "cnt"].sum()],
        }
    )
    rest = table.loc[~is_na, ["value", "pcnt", "cnt"]]
    return pd.concat([nan_row, rest], ignore_index=True)


def _colour_subset(subset: pd.DataFrame, fill: str, right: bool = True) -> p9.geom_col:
    """Build a layer that recolours the given blocks of the stacked bars.

    Each block is drawn as a stack of a transparent spacer and a solid block
    so that it lands in the right place along the bar.
    """
    solid = subset.assign(alpha=100).reset_index(drop=True)
    spacer = solid.drop(columns=["alpha", "cum_perc"]).assign(
        pcnt=lambda d: 100 - d["pcnt"], alpha=0
    )
    blocks = pd.concat([spacer, solid], sort=True)
    blocks = blocks.sort_values(["feature", "alpha"], ascending=right).reset_index(
        drop=True
    )
    return p9.geom_col(
        data=blocks,
        mapping=p9.aes(x="feature", y="pcnt", alpha="alpha"),
        position="stack",
        fill=fill,
        color="black",
        inherit_aes=False,
    )
