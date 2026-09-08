import numpy as np
import pandas as pd

COLUMNS = [
    "col_name",
    "min",
    "q1",
    "median",
    "mean",
    "q3",
    "max",
    "sd",
    "pcnt_na",
    "hist",
]


def test_column_names(starwars, tdf):
    assert starwars.inspect_num().columns.tolist() == COLUMNS
    assert tdf.inspect_num().columns.tolist() == COLUMNS


def test_includes_every_numeric_dtype_but_not_bool(mixed):
    out = mixed.inspect_num()
    assert out["col_name"].tolist() == ["int", "float", "int64_nullable"]


def test_all_numeric_columns_of_tdf(tdf):
    out = tdf.inspect_num()
    assert out["col_name"].tolist() == tdf.select_dtypes("number").columns.tolist()
    assert len(out) == 9


def test_exact_statistics():
    df = pd.DataFrame({"x": [1.0, 2.0, 3.0, 4.0, np.nan]})
    row = df.inspect_num().iloc[0]
    assert row["min"] == 1.0
    assert row["q1"] == 1.75
    assert row["median"] == 2.5
    assert row["mean"] == 2.5
    assert row["q3"] == 3.25
    assert row["max"] == 4.0
    assert np.isclose(row["sd"], np.std([1, 2, 3, 4], ddof=1))
    assert row["pcnt_na"] == 20.0


def test_histogram_structure():
    df = pd.DataFrame({"x": np.linspace(0, 100, 50)})
    hist = df.inspect_num()["hist"][0]
    assert hist.columns.tolist() == ["value", "prop"]
    assert len(hist) == 10
    assert np.isclose(hist["prop"].sum(), 1)
    assert np.allclose(hist["prop"], 0.1)
    # bins are in value order, not frequency order
    assert hist["value"].tolist() == sorted(hist["value"])


def test_constant_missing_and_infinite_columns():
    df = pd.DataFrame(
        {"const": [2.0, 2.0, 2.0], "none": [np.nan] * 3, "inf": [1.0, np.inf, 2.0]}
    )
    out = df.inspect_num().set_index("col_name")
    assert out.loc["const", "sd"] == 0
    assert np.isnan(out.loc["none", "mean"])
    assert out.loc["none", "pcnt_na"] == 100
    assert out.loc["inf", "max"] == np.inf
    shapes = [h.shape for h in out["hist"]]
    assert shapes == [(10, 2), (0, 2), (10, 2)]
    # only the finite values contribute to the histogram
    assert np.isclose(out.loc["inf", "hist"]["prop"].sum(), 1)
