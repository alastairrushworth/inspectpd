"""inspectpd: inspection, comparison and visualisation of pandas data frames.

Importing this package monkey-patches a family of ``inspect_*`` methods onto
pandas objects. Two small example datasets (``starwars`` and ``tdf``) are
exposed as lazily loaded module attributes.
"""

from functools import cache
from importlib.resources import files

from pandas import read_csv
from pandas.core.base import PandasObject

from .inspect.inspect_cat import inspect_cat
from .inspect.inspect_cor import inspect_cor
from .inspect.inspect_imb import inspect_imb
from .inspect.inspect_mem import inspect_mem
from .inspect.inspect_na import inspect_na
from .inspect.inspect_num import inspect_num
from .inspect.inspect_types import inspect_types

__all__ = [
    "inspect_cat",
    "inspect_cor",
    "inspect_imb",
    "inspect_mem",
    "inspect_na",
    "inspect_num",
    "inspect_types",
    "load_dataset",
    "starwars",
    "tdf",
]

# monkey-patch the inspect_* functions as methods on pandas objects
PandasObject.inspect_imb = inspect_imb
PandasObject.inspect_na = inspect_na
PandasObject.inspect_types = inspect_types
PandasObject.inspect_mem = inspect_mem
PandasObject.inspect_cat = inspect_cat
PandasObject.inspect_cor = inspect_cor
PandasObject.inspect_num = inspect_num


# read_csv kwargs for each bundled example dataset
_DATASETS = {
    "starwars": {"index_col": 0},
    "tdf": {},
}


@cache
def load_dataset(name):
    """Load a bundled example dataset by name (``"starwars"`` or ``"tdf"``)."""
    if name not in _DATASETS:
        valid = ", ".join(sorted(_DATASETS))
        raise ValueError(f"unknown dataset {name!r}; choose from: {valid}")
    resource = files("inspectpd").joinpath("data", f"{name}.csv")
    with resource.open("rb") as handle:
        return read_csv(handle, **_DATASETS[name])


def __getattr__(name):
    """Lazily expose example datasets as module attributes (PEP 562)."""
    if name in _DATASETS:
        return load_dataset(name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __dir__():
    return sorted(set(globals()) | set(_DATASETS))
