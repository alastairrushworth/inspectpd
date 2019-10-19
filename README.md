
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

## Installation

You can install `inspectpd` using `pip`:

``` r
pip install git+https://github.com/alastairrushworth/inspectpd
```

## Comments? Suggestions? Issues?

The package is in early stages of development, could break and will
change rapidly. A future version will be released to PyPi. In the
meantime, any feedback is definitely welcome\! Feel free to write a
github issue or send me a message on
[twitter](https://twitter.com/rushworth_a).
