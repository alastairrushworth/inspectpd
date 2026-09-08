import numpy as np
import pandas as pd

COLUMNS = ["col_name", "cnt", "common", "common_pcnt", "levels"]


def test_column_names(starwars, tdf):
    assert starwars.inspect_cat().columns.tolist() == COLUMNS
    assert tdf.inspect_cat().columns.tolist() == COLUMNS


def test_level_counts(starwars, tdf):
    assert starwars.inspect_cat()["cnt"].tolist() == [15, 5, 13, 49, 87, 31, 38]
    assert tdf.inspect_cat()["cnt"].tolist() == [
        15,
        58,
        63,
        39,
        24,
        14,
        38,
        106,
        63,
        48,
    ]


def test_includes_every_categorical_dtype(mixed):
    out = mixed.inspect_cat()
    assert out["col_name"].tolist() == ["bool", "boolean", "cat", "obj", "string"]


def test_missing_is_counted_as_a_level():
    df = pd.DataFrame({"a": ["x", "x", None, "y"]})
    out = df.inspect_cat()
    assert out["cnt"].tolist() == [3]
    assert out["common"].tolist() == ["x"]
    assert out["common_pcnt"].tolist() == [50.0]
    levels = out["levels"][0]
    assert levels.columns.tolist() == ["value", "pcnt", "cnt"]
    assert levels["cnt"].tolist() == [2, 1, 1]
    assert levels.index.tolist() == [0, 1, 2]
    assert np.isclose(levels["pcnt"].sum(), 100)


def test_all_missing_column():
    df = pd.DataFrame({"a": pd.Series([None, None], dtype=object)})
    out = df.inspect_cat()
    assert out["cnt"].tolist() == [1]
    assert pd.isna(out["common"][0])
    assert out["common_pcnt"].tolist() == [100.0]


def test_levels_are_sorted_most_common_first(tdf):
    for levels in tdf.inspect_cat()["levels"]:
        assert levels["cnt"].tolist() == sorted(levels["cnt"], reverse=True)


def test_no_categorical_columns():
    out = pd.DataFrame({"a": [1.0, 2.0]}).inspect_cat()
    assert out.shape == (0, 5)
