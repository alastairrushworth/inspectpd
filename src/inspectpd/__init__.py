"""inspectpd: inspection, comparison and visualisation of pandas data frames.

Importing this package adds a family of ``inspect_*`` methods to
:class:`pandas.DataFrame`. The same functions are also available directly,
for example ``inspectpd.inspect_cat(df)``. Two small example datasets
(``starwars`` and ``tdf``) are exposed as lazily loaded module attributes.
"""

from __future__ import annotations

from functools import cache
from importlib.metadata import PackageNotFoundError, version
from importlib.resources import files
from typing import Any

from pandas import DataFrame, read_csv

from .inspect.inspect_cat import inspect_cat
from .inspect.inspect_cor import inspect_cor
from .inspect.inspect_imb import inspect_imb
from .inspect.inspect_mem import inspect_mem
from .inspect.inspect_na import inspect_na
from .inspect.inspect_num import inspect_num
from .inspect.inspect_types import inspect_types
from .inspect_object.inspect_object import InspectFrame

try:
    __version__ = version("inspectpd")
except PackageNotFoundError:  # pragma: no cover - only when not installed
    __version__ = "0+unknown"

__all__ = [
    "InspectFrame",
    "__version__",
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

# Attach the summaries as DataFrame methods. Only DataFrame gets them: they
# have no meaning on Series, Index or GroupBy objects.
DataFrame.inspect_cat = inspect_cat
DataFrame.inspect_cor = inspect_cor
DataFrame.inspect_imb = inspect_imb
DataFrame.inspect_mem = inspect_mem
DataFrame.inspect_na = inspect_na
DataFrame.inspect_num = inspect_num
DataFrame.inspect_types = inspect_types


# read_csv kwargs for each bundled example dataset
_DATASETS: dict[str, dict[str, Any]] = {
    "starwars": {"index_col": 0},
    "tdf": {},
}


@cache
def _read_dataset(name: str) -> DataFrame:
    resource = files("inspectpd").joinpath("data").joinpath(f"{name}.csv")
    with resource.open("rb") as handle:
        return read_csv(handle, **_DATASETS[name])


def load_dataset(name: str) -> DataFrame:
    """Load a bundled example dataset by name.

    Parameters
    ----------
    name : {"starwars", "tdf"}
        ``starwars`` is the Star Wars characters table from the R ``dplyr``
        package; ``tdf`` is a table of Tour de France winners.

    Returns
    -------
    pandas.DataFrame
        A fresh copy each call, so it is safe to modify.
    """
    if name not in _DATASETS:
        valid = ", ".join(sorted(_DATASETS))
        raise ValueError(f"unknown dataset {name!r}; choose from: {valid}")
    return _read_dataset(name).copy()


def __getattr__(name: str) -> Any:
    """Lazily expose example datasets as module attributes (PEP 562)."""
    if name in _DATASETS:
        return load_dataset(name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __dir__() -> list[str]:
    return sorted(set(globals()) | set(_DATASETS))
