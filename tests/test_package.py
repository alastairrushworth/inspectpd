import re
import sys
import time

import pandas as pd
import pytest

import inspectpd as ipd


def test_version_is_pep440_like():
    assert re.match(r"^\d+(\.\d+)*", ipd.__version__)


def test_all_names_resolve():
    for name in ipd.__all__:
        assert getattr(ipd, name) is not None


def test_dir_lists_datasets():
    assert {"starwars", "tdf"} <= set(dir(ipd))


def test_unknown_attribute_raises():
    with pytest.raises(AttributeError, match="no attribute 'nope'"):
        _ = ipd.nope


def test_methods_only_on_dataframe():
    for name in ["inspect_cat", "inspect_cor", "inspect_na", "inspect_types"]:
        assert hasattr(pd.DataFrame, name)
        assert not hasattr(pd.Series, name)
        assert not hasattr(pd.Index, name)


def test_functional_api_matches_methods(tdf):
    pd.testing.assert_frame_equal(ipd.inspect_na(tdf), tdf.inspect_na())
    pd.testing.assert_frame_equal(ipd.inspect_types(tdf), tdf.inspect_types())


def test_plotting_stack_not_imported_eagerly():
    """``import inspectpd`` must not drag in plotnine, matplotlib or scipy.stats."""
    import subprocess

    code = (
        "import sys, inspectpd; "
        "print(sorted(m for m in ('plotnine', 'matplotlib', 'scipy.stats') "
        "if m in sys.modules))"
    )
    out = subprocess.run(
        [sys.executable, "-c", code], capture_output=True, text=True, check=True
    )
    assert out.stdout.strip() == "[]"


@pytest.mark.parametrize("name", ["starwars", "tdf"])
def test_load_dataset_returns_fresh_copy(name):
    first = ipd.load_dataset(name)
    first["_probe"] = 1
    second = ipd.load_dataset(name)
    assert "_probe" not in second.columns
    assert "_probe" not in getattr(ipd, name).columns


def test_load_dataset_is_cached():
    ipd.load_dataset("tdf")
    start = time.perf_counter()
    ipd.load_dataset("tdf")
    assert time.perf_counter() - start < 0.05


def test_load_dataset_unknown_name():
    with pytest.raises(ValueError, match="choose from: starwars, tdf"):
        ipd.load_dataset("penguins")


def test_dataset_shapes(starwars, tdf):
    assert starwars.shape == (87, 10)
    assert tdf.shape == (106, 19)
