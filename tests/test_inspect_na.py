import numpy as np
import pandas as pd

COLUMNS = ["col_name", "cnt", "pcnt"]


def test_column_names(starwars, tdf):
    assert starwars.inspect_na().columns.tolist() == COLUMNS
    assert tdf.inspect_na().columns.tolist() == COLUMNS


def test_counts(starwars, tdf):
    assert starwars.inspect_na()["cnt"].tolist() == [44, 28, 10, 6, 5, 5, 3, 0, 0, 0]
    assert tdf.inspect_na()["cnt"].tolist() == [60, 50, 40, 39, 32, 8, 8] + [0] * 12


def test_matches_pandas(tdf):
    out = tdf.inspect_na().set_index("col_name")
    expected = tdf.isna().sum()
    assert out.loc[expected.index, "cnt"].tolist() == expected.tolist()
    assert np.allclose(out.loc[expected.index, "pcnt"], 100 * tdf.isna().mean())


def test_sorted_descending_with_fresh_index(mixed):
    out = mixed.inspect_na()
    assert out["pcnt"].tolist() == sorted(out["pcnt"], reverse=True)
    assert out.index.tolist() == list(range(mixed.shape[1]))


def test_exact_values():
    df = pd.DataFrame({"a": [1.0, np.nan, np.nan, 4.0], "b": ["x", None, "y", "z"]})
    out = df.inspect_na()
    assert out["col_name"].tolist() == ["a", "b"]
    assert out["cnt"].tolist() == [2, 1]
    assert out["pcnt"].tolist() == [50.0, 25.0]
