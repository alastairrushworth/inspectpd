import scipy.stats as st
import pandas as pd
import numpy as np
from inspectpd.inspect_object.inspect_object import inspect_object

def inspect_cor(df, method='pearson', alpha=0.05, with_col=None) :
  '''
  Tidy correlation coefficients for numeric dataframe columns.
  
  Parameters
  ----------
  
  df: A pandas dataframe.
  
  method: str, default 'pearson'
    a character string indicating which type of correlation 
    coefficient to use, one of "pearson", "kendall", or "spearman".

  alpha: float, default 0.05.
    Alpha level for correlation confidence intervals. Defaults to 0.05.
  
  with_col: str, default None
    Column name to filter correlations by.  Uses pandas .withcorr() under
    the hood instead of .corr(), which can save time for large data sets.
    
  Returns  
  ----------
  
  A pandas dataframe with columns
    + col_1, co1_2: object 
      character columns containing names of numeric columns in df1.
    + corr: float64
      columns of correlation coefficients
    + p_value: float64
      p-value associated with a test where the null hypothesis is 
      that the numeric pair have 0 correlation.
    + lower, upper: float64
      lower and upper values of the confidence interval for the correlations.
    + pcnt_na: 
      the number of pairs of observations that were non missing for each 
      pair of columns. The correlation calculation used by .inspect_cor() 
      uses only pairwise complete observations.
  '''
  df_num = df.select_dtypes('number').copy()
  if with_col is None :
    out = df_num.corr(method = method)
    # get the number of variables
    nvarb = out.shape[0]
    # unpivot the correlation matrix
    out = out.unstack().reset_index(drop = False)
    # rename columns
    out.columns = ['col_1', 'col_2', 'corr']
    # row index of off diagonal elements
    inds = [(np.arange(i + 1) + i * nvarb).tolist() for i in range(nvarb)]
    inds  = [j for i in inds for j in i]
    # drop off diagonals
    out = out[~out.index.isin(inds)].reset_index(drop = True)
  else :
    out = df_num.corrwith(df_num[with_col]).reset_index(drop = False)
    out['col_2'] = with_col
    # rename columns and reorder
    out.columns = ['col_1', 'corr', 'col_2']
    out = out[['col_1', 'col_2', 'corr']]

  # remove self-correlations
  out = out.query('col_1 != col_2').reset_index(drop = True)
  # get pairwise non-na
  df_null    = 1 - df_num.isnull().astype('int')
  nna_mat    = df_null.transpose().dot(df_null)
  nna_df     = nna_mat.unstack().reset_index(drop = False)
  nna_df.columns = ['col_1', 'col_2', 'nna']
  # add standard errors
  nna_df = nna_df.assign(se = (1 / np.sqrt(nna_df.nna - 3)))
  nna_df     = nna_df \
    .assign(pcnt_na = 100 * nna_df.nna / df.shape[0]) \
    .drop('nna', axis = 1)
  # join pairwise nna to the output df
  out = out.merge(nna_df, how = 'left', on = ['col_1', 'col_2'])
  out['p_value'] = 2 * st.norm.cdf(-np.abs(out['corr'].values / out.se))
  # swicth off divide by zero error pinged by numpy with arctans
  np.seterr(all = 'ignore') 
  out['lower'] = np.tanh(np.arctanh(out['corr'].values) - st.norm.ppf(1 - alpha / 2) * out.se)
  out['upper'] = np.tanh(np.arctanh(out['corr'].values) + st.norm.ppf(1 - alpha / 2) * out.se)
  np.seterr(all = 'warn') 
  # sort by absolute value of corr
  out = out \
    .assign(abs_cor = np.abs(out['corr'].values)) \
    .sort_values('abs_cor', ascending = False) \
    .drop(['abs_cor', 'se'], axis = 1) \
    .reset_index(drop = True)
  # change order of output columns
  out = out[['col_1', 'col_2', 'corr', 'p_value', 'lower', 'upper', 'pcnt_na']]
  # add type attribute to output
  out = inspect_object(out, my_attr = 'inspect_cor')
  return out
  
  
  
  
