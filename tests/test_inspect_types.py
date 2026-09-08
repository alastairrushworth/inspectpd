import numpy as np
import pandas as pd

COLUMNS = ["type", "cnt", "pcnt", "col_name"]


def test_column_names(starwars, tdf):
    assert starwars.inspect_types().columns.tolist() == COLUMNS
    assert tdf.inspect_types().columns.tolist() == COLUMNS


def test_all_columns_summarised(starwars, tdf):
    for df in (starwars, tdf):
        out = df.inspect_types()
        assert out["cnt"].sum() == df.shape[1]
        assert np.isclose(out["pcnt"].sum(), 100)
        assert sorted(c for cols in out["col_name"] for c in cols) == sorted(df.columns)


def test_types_are_strings_sorted_by_count_with_fresh_index(mixed):
    out = mixed.inspect_types()
    assert all(isinstance(t, str) for t in out["type"])
    assert out["cnt"].tolist() == sorted(out["cnt"], reverse=True)
    assert out.index.tolist() == list(range(len(out)))


def test_exact_values():
    df = pd.DataFrame({"a": [1, 2], "b": [3, 4], "c": [1.0, 2.0]})
    out = df.inspect_types()
    assert out["type"].tolist() == ["int64", "float64"]
    assert out["cnt"].tolist() == [2, 1]
    assert out["col_name"].tolist() == [["a", "b"], ["c"]]
    assert np.allclose(out["pcnt"], [200 / 3, 100 / 3])
