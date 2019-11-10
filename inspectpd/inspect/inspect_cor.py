import scipy.stats as st
import pandas as pd
import numpy as np
from inspectpd.inspect_object.inspect_object import inspect_object

def inspect_cor(df, method = 'pearson', alpha = 0.05) :
  out = df.corr(method = method)
  # get the number of variables
  nvarb = out.shape[0]
  # unpivot the correlation matrix
  out = out.unstack().reset_index(drop = False)
  out.columns = ['col_1', 'col_2', 'corr']
  # row index of off diagonal elements
  inds = [(np.arange(i + 1) + i * nvarb).tolist() for i in range(nvarb)]
  inds  = [j for i in inds for j in i]
  # drop off diagonals
  out = out[~out.index.isin(inds)].reset_index(drop = True)
  # get pairwise non-na
  cor_cols   = list(set(out.col_1.to_list() + out.col_2.to_list()))
  df_numeric = df[cor_cols]
  df_null    = 1 - df_numeric.isnull().astype('int')
  nna_mat    = df_null.transpose().dot(df_null)
  nna_df     = nna_mat.unstack().reset_index(drop = False)
  nna_df.columns = ['col_1', 'col_2', 'nna']
  # add standard errors
  nna_df = nna_df.assign(se = (1 / np.sqrt(nna_df.nna - 3)))
  nna_df     = nna_df\
    .assign(pcnt_nna = 100 * nna_df.nna / df.shape[0])\
    .drop('nna', axis = 1)
  # join pairwise nna to the output df
  out = out.merge(nna_df, how = 'left', on = ['col_1', 'col_2'])
  out['p_value'] = 2 * st.norm.cdf(-np.abs(out['corr'].values / out.se))
  out['lower'] = np.tanh(np.arctanh(out['corr'].values) - st.norm.ppf(1 - alpha / 2) * out.se)
  out['upper'] = np.tanh(np.arctanh(out['corr'].values) + st.norm.ppf(1 - alpha / 2) * out.se)
  # sort by absolute value of corr
  out = out\
    .assign(abs_cor = np.abs(out['corr'].values))\
    .sort_values('abs_cor', ascending = False)\
    .drop(['abs_cor', 'se'], axis = 1)\
    .reset_index(drop = True)
  # add type attribute to output
  out.type = 'inspect_cor'
  return out
  
  
  
  
