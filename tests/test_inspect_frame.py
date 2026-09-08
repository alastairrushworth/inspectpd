import pandas as pd
import pytest

import inspectpd as ipd
from inspectpd import InspectFrame
from inspectpd.inspect_object.inspect_object import inspect_object


def test_result_is_inspect_frame(tdf):
    out = tdf.inspect_na()
    assert isinstance(out, InspectFrame)
    assert isinstance(out, pd.DataFrame)
    assert out.inspect_type == "inspect_na"
    assert out.inspect_params == {}


def test_legacy_class_alias():
    assert inspect_object is InspectFrame


@pytest.mark.parametrize(
    "op",
    [
        lambda df: df.head(3),
        lambda df: df.iloc[:2],
        lambda df: df.copy(),
        lambda df: df.sort_values("col_name"),
        lambda df: df[df["pcnt"] > 0],
        lambda df: pd.concat([df, df]),
    ],
)
def test_metadata_survives_pandas_ops(tdf, op):
    out = op(tdf.inspect_na())
    assert isinstance(out, InspectFrame)
    assert out.inspect_type == "inspect_na"


def test_params_survive_slicing(tdf):
    out = tdf.inspect_cor(method="spearman", alpha=0.1).head(2)
    assert out.inspect_params["method"] == "spearman"
    assert out.inspect_params["alpha"] == 0.1


def test_view_unknown_type_raises():
    frame = InspectFrame(pd.DataFrame({"a": [1]}))
    with pytest.raises(ValueError, match="inspect_type=None"):
        frame.view()


def test_series_input_raises(starwars):
    with pytest.raises(TypeError, match="got Series"):
        ipd.inspect_na(starwars["name"])


@pytest.mark.parametrize(
    "func",
    [
        ipd.inspect_cat,
        ipd.inspect_cor,
        ipd.inspect_imb,
        ipd.inspect_mem,
        ipd.inspect_na,
        ipd.inspect_num,
        ipd.inspect_types,
    ],
)
def test_duplicate_column_names_raise(func):
    df = pd.DataFrame([[1.0, 2.0, "x"]], columns=["a", "a", "b"])
    with pytest.raises(ValueError, match=r"duplicated: \['a'\]"):
        func(df)


EMPTY_SHAPES = {
    "inspect_types": (0, 4),
    "inspect_na": (0, 3),
    "inspect_mem": (0, 4),
    "inspect_cat": (0, 5),
    "inspect_imb": (0, 4),
    "inspect_num": (0, 10),
    "inspect_cor": (0, 7),
}


@pytest.mark.parametrize(("name", "shape"), EMPTY_SHAPES.items())
def test_empty_frame_gives_empty_summary(name, shape):
    out = getattr(pd.DataFrame(), name)()
    assert out.shape == shape
    assert out.inspect_type == name
    with pytest.raises(ValueError, match="to view"):
        out.view()
