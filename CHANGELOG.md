# Changelog

All notable changes to this project are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Breaking changes

- `inspect_cor()`: the `pcnt_na` column is renamed `pcnt_nna`. It always
  reported the percentage of *non-missing* pairs, so the old name was
  misleading.
- `inspect_cor().view()`: the `max` keyword is renamed `max_pairs`.
- The `inspect_*` methods are now attached to `pandas.DataFrame` only. They
  previously appeared on Series, Index and GroupBy objects too, where they
  crashed with unhelpful errors.
- `inspect_types()`: the `type` column now holds dtype names as strings rather
  than dtype objects, and the result index is reset.
- `inspect_num()` now includes every numeric dtype (integer, float32, nullable
  `Int64`/`Float64`); it previously only summarised float64 columns.
- `inspect_cat()` and `inspect_imb()` now include boolean columns and the
  nullable `string` dtype alongside `category`, `object` and `str` columns.
- `inspect_num()`: the `value` column of each `hist` table has interval dtype
  rather than being a categorical of intervals.
- `inspect_mem()`: the `size` column uses binary unit labels (`KiB`, `MiB`)
  to match the 1024-based arithmetic it always used.
- Inputs must be data frames with unique column names; anything else raises
  `TypeError` or `ValueError` up front instead of failing part way through.
- Empty summaries raise `ValueError` from `.view()` rather than `RuntimeError`.

### Fixed

- `inspect_cor().view()` labelled every bar with the wrong column pair: the
  axis was sorted alphabetically while the bars were positioned by rank.
- `inspect_types().view()` crashed on pandas 3.
- `inspect_cor(with_col=...)` ignored the `method` argument and always
  returned Pearson correlations.
- `inspect_cor()` p-values are now computed on the Fisher z scale, so they
  agree with the confidence intervals on the same row. Spearman and Kendall
  coefficients use their own standard errors, pairs with too few observations
  return `NaN` instead of misleading values, and the plot colours pairs using
  the `alpha` the summary was computed with rather than a hard-coded 0.05.
- `inspect_cor()` no longer overwrites the global numpy floating-point error
  settings.
- `inspect_num().view()` no longer adds a column to the histogram tables
  stored in the summary it was called on.
- `inspect_imb()` crashed on a column that was entirely missing.
- `inspect_num()` crashed on columns that were entirely missing or contained
  infinity.
- `inspect_cor().view()` crashed when column names were not strings.
- `inspect_types().view()` left some bars unlabelled.
- `inspect_cat()` and `inspect_imb()` no longer rely on deprecated pandas
  behaviour to find `str` columns, which would have silently dropped them in
  pandas 4.
- Building from a checkout failed when any non-release tag pointed at the
  current commit; release tags are now matched with an explicit pattern.

### Added

- `inspectpd.__version__`.
- Type hints throughout and a `py.typed` marker.
- `InspectFrame`, the result type, is exported. Results carry
  `inspect_type` and `inspect_params` metadata through pandas operations.
- `load_dataset()` returns a fresh copy each call, so modifying
  `inspectpd.starwars` no longer affects later uses.
- A full test suite covering every summary, every plot and the edge cases
  above, run with warnings as errors on Python 3.10 to 3.14 and on the
  lowest supported dependency versions.
- Minimum dependency versions are declared (`pandas>=2.2.2`, `numpy>=1.26`,
  `plotnine>=0.13`, `scipy>=1.11.2`).

### Changed

- `import inspectpd` is roughly four times faster: plotnine and scipy.stats
  are imported only when first needed.
- The four bar-chart plots share one implementation.
- README rewritten with an example and plot for every summary.

## [0.2.0] - 2026-06-06

- Modernised packaging: `pyproject.toml` with hatchling, `src` layout, uv,
  pre-commit with ruff, automated PyPI releases from git tags.
- Dropped Python 3.9.

## [0.1.0] - 2025-01-26

- Initial release.
