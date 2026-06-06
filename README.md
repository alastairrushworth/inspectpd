
# inspectpd

## Overview

`inspectpd` is collection of utilities for columnwise summary,
comparison and visualisation of `pandas` dataframes. The package patches
in the following methods for pandas objects:

  - [`.inspect_types()`](#column-types) summary of column types
  - [`.inspect_mem()`](#memory-usage) summary of memory usage of columns
  - [`.inspect_na()`](#missing-values) columnwise prevalence of missing
    values
  - [`.inspect_cor()`](#correlation) correlation coefficients of numeric
    columns
  - [`.inspect_imb()`](#feature-imbalance) feature imbalance of
    non-numeric
  - [`.inspect_num()`](#numeric-summaries) summaries of numeric columns
  - [`.inspect_cat()`](#categorical-levels) summaries of non-numeric

## Installation and use

You can install `inspectpd` using `pip` with

```python
pip install inspectpd
```

Simply import the package and use the methods on a pandas dataframe:

```
import pandas as pd
import inspectpd
# example data set just for illustration
from inspectpd import starwars

# categorical features summary
starwars.inspect_cat()
```

You can also get a quick visualisation of the summary too:

```
# get a plot of the categorical features
starwars.inspect_cat().view()
```

## Development

This project uses [uv](https://docs.astral.sh/uv/) for environment management
and [pre-commit](https://pre-commit.com/) with [ruff](https://docs.astral.sh/ruff/)
for linting and formatting.

```bash
# create the dev environment and install inspectpd (editable) + dev tools
uv sync

# install the git hooks
uv run pre-commit install

# run the test suite
uv run pytest

# lint and format
uv run ruff check .
uv run ruff format .

# build the sdist and wheel
uv build
```
