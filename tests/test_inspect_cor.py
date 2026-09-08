import numpy as np
import pandas as pd
import pytest
from scipy import stats

COLUMNS = ["col_1", "col_2", "corr", "p_value", "lower", "upper", "pcnt_nna"]


def test_column_names(starwars, tdf):
    assert starwars.inspect_cor().columns.tolist() == COLUMNS
    assert tdf.inspect_cor().columns.tolist() == COLUMNS


def test_one_row_per_pair(tdf):
    k = tdf.select_dtypes("number").shape[1]
    out = tdf.inspect_cor()
    assert len(out) == k * (k - 1) // 2
    pairs = {frozenset(p) for p in zip(out["col_1"], out["col_2"], strict=True)}
    assert len(pairs) == len(out)
    assert (out["col_1"] != out["col_2"]).all()


@pytest.mark.parametrize("method", ["pearson", "kendall", "spearman"])
def test_matches_pandas_corr(tdf, method):
    out = tdf.inspect_cor(method=method)
    expected = tdf.select_dtypes("number").corr(method=method)
    for a, b, r in zip(out["col_1"], out["col_2"], out["corr"], strict=True):
        assert np.isclose(r, expected.at[a, b], equal_nan=True)


def test_sorted_by_absolute_correlation(tdf):
    out = tdf.inspect_cor()
    abs_corr = out["corr"].abs().dropna()
    assert abs_corr.tolist() == sorted(abs_corr, reverse=True)
    assert out.index.tolist() == list(range(len(out)))


def test_stores_parameters(tdf):
    out = tdf.inspect_cor(method="spearman", alpha=0.1, with_col="edition")
    assert out.inspect_type == "inspect_cor"
    assert out.inspect_params == {
        "method": "spearman",
        "alpha": 0.1,
        "with_col": "edition",
    }


@pytest.mark.parametrize("method", ["pearson", "spearman"])
def test_with_col_matches_full_matrix(tdf, method):
    full = tdf.inspect_cor(method=method)
    sub = tdf.inspect_cor(method=method, with_col="edition")
    assert (sub["col_2"] == "edition").all()
    assert len(sub) == tdf.select_dtypes("number").shape[1] - 1
    for _, row in sub.iterrows():
        match = full[
            ((full["col_1"] == row["col_1"]) & (full["col_2"] == "edition"))
            | ((full["col_2"] == row["col_1"]) & (full["col_1"] == "edition"))
        ].iloc[0]
        assert np.isclose(row["corr"], match["corr"])
        assert np.isclose(row["p_value"], match["p_value"])
        assert np.isclose(row["pcnt_nna"], match["pcnt_nna"])


def test_with_col_must_be_numeric(tdf):
    with pytest.raises(ValueError, match="not a numeric column"):
        tdf.inspect_cor(with_col="winner_name")
    with pytest.raises(ValueError, match="not a numeric column"):
        tdf.inspect_cor(with_col="missing")


def test_invalid_method_and_alpha(tdf):
    with pytest.raises(ValueError, match="method must be one of"):
        tdf.inspect_cor(method="cosine")
    for alpha in (0, 1, -0.1, 1.5):
        with pytest.raises(ValueError, match="alpha must be"):
            tdf.inspect_cor(alpha=alpha)


def test_pcnt_nna_is_percentage_of_complete_pairs():
    df = pd.DataFrame(
        {
            "a": [1.0, 2.0, 3.0, 4.0, np.nan, np.nan, 7.0, 8.0, 9.0, 10.0],
            "b": np.arange(10.0),
            "c": [np.nan, *np.arange(9.0)],
        }
    )
    out = df.inspect_cor().set_index(["col_1", "col_2"])
    assert out.loc[("a", "b"), "pcnt_nna"] == 80.0
    assert out.loc[("a", "c"), "pcnt_nna"] == 70.0
    assert out.loc[("b", "c"), "pcnt_nna"] == 90.0


def test_fisher_z_p_value_and_interval():
    rng = np.random.default_rng(0)
    x = rng.normal(size=40)
    y = 0.5 * x + rng.normal(size=40)
    row = pd.DataFrame({"x": x, "y": y}).inspect_cor().iloc[0]
    r = np.corrcoef(x, y)[0, 1]
    se = 1 / np.sqrt(40 - 3)
    z = np.arctanh(r)
    assert np.isclose(row["corr"], r)
    assert np.isclose(row["p_value"], 2 * stats.norm.sf(abs(z) / se))
    assert np.isclose(row["lower"], np.tanh(z - stats.norm.ppf(0.975) * se))
    assert np.isclose(row["upper"], np.tanh(z + stats.norm.ppf(0.975) * se))
    # close to the exact t-test for a sample of this size
    assert abs(row["p_value"] - stats.pearsonr(x, y).pvalue) < 0.01


def test_p_value_agrees_with_interval():
    """A pair is significant at alpha exactly when its interval excludes zero."""
    rng = np.random.default_rng(1)
    df = pd.DataFrame(rng.normal(size=(15, 8)))
    df[0] = df[1] * 0.6 + rng.normal(size=15) * 0.8
    for alpha in (0.05, 0.2):
        out = df.inspect_cor(alpha=alpha)
        significant = out["p_value"] < alpha
        excludes_zero = (out["lower"] > 0) | (out["upper"] < 0)
        assert (significant == excludes_zero).all()


def test_alpha_changes_interval_width(tdf):
    narrow = tdf.inspect_cor(alpha=0.2)
    wide = tdf.inspect_cor(alpha=0.01)
    assert (
        (wide["upper"] - wide["lower"]) >= (narrow["upper"] - narrow["lower"])
    ).all()


def test_too_few_observations_give_nan_not_garbage():
    df = pd.DataFrame(
        {
            "a": [1.0, 2.0, 3.0, np.nan],
            "b": [1.0, 3.0, 2.0, np.nan],
            "c": [1.0, 2.0, 3.0, 4.0],
        }
    )
    out = df.inspect_cor()
    assert out["p_value"].isna().all()
    assert out["lower"].isna().all()
    assert out["upper"].isna().all()
    assert (out["pcnt_nna"] == 75.0).all()


def test_kendall_needs_five_observations():
    df = pd.DataFrame({"a": [1.0, 2.0, 3.0, 4.0], "b": [1.0, 3.0, 2.0, 4.0]})
    assert df.inspect_cor(method="kendall")["p_value"].isna().all()
    df = pd.DataFrame({"a": [1.0, 2.0, 3.0, 4.0, 5.0], "b": [1.0, 3.0, 2.0, 4.0, 5.0]})
    assert df.inspect_cor(method="kendall")["p_value"].notna().all()


def test_numpy_error_state_is_restored(tdf):
    old = np.seterr(all="raise")
    try:
        tdf.inspect_cor()
        assert np.geterr() == {k: "raise" for k in old}
    finally:
        np.seterr(**old)


def test_perfect_correlation():
    df = pd.DataFrame({"a": [1.0, 2.0, 3.0, 4.0, 5.0], "b": [2.0, 4.0, 6.0, 8.0, 10.0]})
    row = df.inspect_cor().iloc[0]
    assert row["corr"] == 1.0
    assert row["p_value"] == 0.0
    assert row["upper"] == 1.0


def test_no_numeric_columns(starwars):
    out = starwars[["name", "gender"]].inspect_cor()
    assert out.shape == (0, 7)
    assert out.columns.tolist() == COLUMNS
    assert starwars[["name", "height"]].inspect_cor().shape == (0, 7)


def test_nullable_and_integer_columns(mixed):
    out = mixed.inspect_cor()
    assert len(out) == 3
    assert out["corr"].notna().all()
