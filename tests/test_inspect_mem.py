import numpy as np
import pytest

from inspectpd.inspect.inspect_mem import format_size

COLUMNS = ["col_name", "bytes", "size", "pcnt"]


def test_column_names(starwars, tdf):
    assert starwars.inspect_mem().columns.tolist() == COLUMNS
    assert tdf.inspect_mem().columns.tolist() == COLUMNS


def test_matches_pandas_memory_usage(tdf):
    out = tdf.inspect_mem().set_index("col_name")
    usage = tdf.memory_usage(index=False, deep=True)
    assert out.loc[usage.index, "bytes"].tolist() == usage.tolist()
    assert np.isclose(out["pcnt"].sum(), 100)


def test_sorted_descending(mixed):
    out = mixed.inspect_mem()
    assert out["bytes"].tolist() == sorted(out["bytes"], reverse=True)
    assert out.index.tolist() == list(range(mixed.shape[1]))
    assert all(isinstance(s, str) for s in out["size"])


@pytest.mark.parametrize(
    ("num", "expected"),
    [
        (0, "  0 B"),
        (512, "512 B"),
        (1024, "1.00 KiB"),
        (1536, "1.50 KiB"),
        (5 * 1024**2, "5.00 MiB"),
        (2 * 1024**8, "2.00 YiB"),
        (5000 * 1024**8, "5000.00 YiB"),
    ],
)
def test_format_size(num, expected):
    assert format_size(num) == expected
