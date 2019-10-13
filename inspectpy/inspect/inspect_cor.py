import pandas as pd
import numpy as np

# todo
# --> pvalues and confidence intervals

def inspect_cor(df) :
  out = df.corr()
  # get the number of variables
  nvarb = out.shape[0]
  # unpivot the correlation matrix
  out = out.unstack().reset_index(drop = False)
  out.columns = ['col_1', 'col_2', 'corr']
  # row index of off diagonal elements
  inds = [(np.arange(i + 1) + i * nvarb).tolist() for i in range(nvarb)]
  inds  = [j for i in inds for j in i]
  # drop off diagonals
  out = out[~out.index.isin(inds)]
  # to add.  pvalues and confidence regions
  out['p_value'] = None
  out['lower'] = None
  out['upper'] = None
  # sort from highest to lowest according to absolute value
  out['abs'] = np.abs(out['corr'])
  out = out.sort_values('abs', ascending = False)
  out = out.drop('abs', axis = 1).reset_index(drop = True)
  # add type attribute to output
  out.type = 'inspect_cor'
  return out
