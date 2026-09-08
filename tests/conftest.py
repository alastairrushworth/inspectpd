import matplotlib
import numpy as np
import pandas as pd
import pytest

import inspectpd as ipd

# render plots off-screen in tests
matplotlib.use("Agg")


@pytest.fixture(scope="session")
def starwars() -> pd.DataFrame:
    return ipd.load_dataset("starwars")


@pytest.fixture(scope="session")
def tdf() -> pd.DataFrame:
    return ipd.load_dataset("tdf")


@pytest.fixture
def mixed() -> pd.DataFrame:
    """A small frame exercising every dtype family the package handles."""
    return pd.DataFrame(
        {
            "int": [1, 2, 3, 4, 5, 6],
            "float": [1.5, np.nan, 3.5, 4.5, 5.5, 6.5],
            "int64_nullable": pd.array([1, None, 3, 4, 5, 6], dtype="Int64"),
            "obj": ["a", "a", "b", None, "c", "a"],
            "string": pd.Series(["x", "y", "x", "x", None, "y"], dtype="string"),
            "cat": pd.Categorical(["u", "v", "u", "u", "u", "w"]),
            "bool": [True, False, True, True, False, True],
            "boolean": pd.array([True, None, True, False, True, True], dtype="boolean"),
        }
    )


@pytest.fixture
def draw():
    """Draw a plotnine object to a matplotlib Figure, then close it."""
    import matplotlib.pyplot as plt

    figures = []

    def _draw(plot):
        fig = plot.draw()
        figures.append(fig)
        return fig

    yield _draw
    for fig in figures:
        plt.close(fig)
