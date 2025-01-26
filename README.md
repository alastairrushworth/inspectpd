
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

You can install `inspectpd` using `pip`:

```python
pip install git+https://github.com/alastairrushworth/inspectpd
```

Simply import the package and use the methods on a pandas dataframe:

```
import inspectpd
# example data set for illustration
from inspectpd import starwars

# categorical features summary
starwars.inspect_cat()
```

You can also get a quick visualisation of the summary too:

```
# get a plot of the categorical features
starwars.inspect_cat().view()
```
