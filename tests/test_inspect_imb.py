import numpy as np
import pandas as pd

COLUMNS = ["col_name", "value", "cnt", "pcnt"]


def test_column_names(starwars, tdf):
    assert starwars.inspect_imb().columns.tolist() == COLUMNS
    assert tdf.inspect_imb().columns.tolist() == COLUMNS


def test_exact_values():
    df = pd.DataFrame(
        {"a": ["x", "x", "y", None], "b": ["p", "q", "r", "p"], "c": [True] * 4}
    )
    out = df.inspect_imb()
    assert out["col_name"].tolist() == ["c", "a", "b"]
    assert out["value"].tolist() == [True, "x", "p"]
    assert out["cnt"].tolist() == [4, 2, 2]
    # missing values are excluded from the denominator
    assert np.allclose(out["pcnt"], [100.0, 200 / 3, 50.0])


def test_sorted_descending_with_fresh_index(tdf):
    out = tdf.inspect_imb()
    assert out["pcnt"].tolist() == sorted(out["pcnt"], reverse=True)
    assert out.index.tolist() == list(range(len(out)))


def test_all_missing_column_does_not_crash():
    df = pd.DataFrame({"a": ["x", "y", "x"], "b": pd.Series([None] * 3, dtype=object)})
    out = df.inspect_imb()
    row = out.set_index("col_name").loc["b"]
    assert pd.isna(row["value"])
    assert row["cnt"] == 0
    assert np.isnan(row["pcnt"])


def test_includes_every_categorical_dtype(mixed):
    assert sorted(mixed.inspect_imb()["col_name"]) == [
        "bool",
        "boolean",
        "cat",
        "obj",
        "string",
    ]
