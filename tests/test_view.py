import matplotlib.figure
import numpy as np
import pandas as pd
import pytest

import inspectpd as ipd

SUMMARIES = [
    "inspect_types",
    "inspect_na",
    "inspect_mem",
    "inspect_cat",
    "inspect_imb",
    "inspect_num",
    "inspect_cor",
]


@pytest.mark.parametrize("dataset", ["starwars", "tdf"])
@pytest.mark.parametrize("name", SUMMARIES)
def test_every_view_renders(dataset, name, draw):
    df = ipd.load_dataset(dataset)
    fig = draw(getattr(df, name)().view())
    assert isinstance(fig, matplotlib.figure.Figure)


def test_views_render_on_mixed_dtypes(mixed, draw):
    for name in SUMMARIES:
        draw(getattr(mixed, name)().view())


def _ytick_labels(fig):
    return [t.get_text() for t in fig.axes[0].get_yticklabels()]


def test_view_cor_labels_match_bar_order(tdf, draw):
    out = tdf.inspect_cor()
    fig = draw(out.view(max_pairs=6))
    expected = [
        f"{a} & {b}" for a, b in zip(out["col_1"][:6], out["col_2"][:6], strict=True)
    ]
    # coord_flip puts the first (strongest) pair at the top
    assert _ytick_labels(fig) == expected[::-1]


def test_view_cor_max_pairs(tdf, draw):
    out = tdf.inspect_cor()
    assert len(_ytick_labels(draw(out.view(max_pairs=3)))) == 3
    assert (
        len(_ytick_labels(draw(out.view(max_pairs=None)))) == out["corr"].notna().sum()
    )


def test_view_cor_legacy_max_keyword_rejected(tdf):
    with pytest.raises(TypeError):
        tdf.inspect_cor().view(max=3)


def test_view_cor_colours_use_summary_alpha(tdf):
    strict = tdf.inspect_cor(alpha=1e-12).view()
    lax = tdf.inspect_cor(alpha=0.5).view()
    assert strict.labels.get("fill", None) == "p < 1e-12"
    assert lax.labels.get("fill", None) == "p < 0.5"
    assert (strict.data["significant"] == "yes").sum() < (
        lax.data["significant"] == "yes"
    ).sum()


def test_view_cor_with_integer_column_names(draw):
    df = pd.DataFrame(np.random.default_rng(1).normal(size=(20, 3)))
    out = df.inspect_cor()
    fig = draw(out.view())
    expected = [f"{a} & {b}" for a, b in zip(out["col_1"], out["col_2"], strict=True)]
    assert _ytick_labels(fig) == expected[::-1]


def test_view_cor_all_nan_raises():
    df = pd.DataFrame({"a": [1.0, np.nan], "b": [np.nan, 1.0]})
    with pytest.raises(ValueError, match="all correlations are NaN"):
        df.inspect_cor().view()


def test_view_cor_pairs_without_interval_still_draw(draw):
    df = pd.DataFrame({"a": [1.0, 2.0, 3.0], "b": [1.0, 3.0, 2.0]})
    draw(df.inspect_cor().view())


def test_view_num_does_not_mutate_summary(tdf, draw):
    out = tdf.inspect_num()
    before = [h.copy() for h in out["hist"]]
    draw(out.view())
    for old, new in zip(before, out["hist"], strict=True):
        pd.testing.assert_frame_equal(old, new)


def test_view_num_skips_columns_without_finite_values(draw):
    df = pd.DataFrame({"a": [1.0, 2.0, 3.0], "b": [np.nan] * 3})
    draw(df.inspect_num().view())
    with pytest.raises(ValueError, match="finite values"):
        pd.DataFrame({"b": [np.nan] * 3}).inspect_num().view()


def test_view_cat_high_cardinality(starwars, draw):
    out = starwars.inspect_cat()
    plot = out.view(high_cardinality=5)
    draw(plot)
    assert (plot.data["value"] == "High cardinality").sum() == len(out)
    # the summary itself is untouched
    assert "feature" not in out["levels"][0].columns


def test_view_cat_without_missing_values(draw):
    df = pd.DataFrame({"a": ["x", "y", "x"], "b": ["p", "p", "p"]})
    draw(df.inspect_cat().view())


def test_view_types_labels_every_bar(draw):
    df = pd.DataFrame({"a": [1], "b": [1], "c": [1], "d": [1], "e": [1.0], "f": ["x"]})
    fig = draw(df.inspect_types().view())
    labels = sorted(t.get_text() for t in fig.axes[0].texts)
    assert labels == ["1", "1", "4"]


def test_view_on_sliced_summary(tdf, draw):
    draw(tdf.inspect_na().head(3).view())
    draw(tdf.inspect_cor().iloc[:4].view())
