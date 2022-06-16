import pandas as pd
import numpy as np
from inspectpd.inspect_object.inspect_object import inspect_object

# inspect_cat  
def inspect_cat(df) :
  '''
  Summary and comparison of the levels in categorical columns
  
  Parameters
  ----------
  
  df: A pandas dataframe.
  
  Returns  
  ----------
  
  A pandas dataframe with columns:
    + col_name: object
      column of strings containing column names of df
    + cnt: int64
      integer column containing count of unique levels 
      found in each column of df.
    + common: object
      column of strings containing the name of the most common level
    + common_pcnt: float64
      the percentage of each column occupied by the most common level 
      shown in common.
    + levels: object
      a list containing relative frequency dataframes for each column in df.
  '''
  
  # get the string / categorical columns
  df_cat = df.select_dtypes(['category', 'object'])
  # new df with columns names as first col
  out = pd.DataFrame(df_cat.columns, columns = ['col_name'])
  # tabulate values in each column
  levels_list = []
  for col in df_cat.columns :
    col_vals = df_cat[col] \
      .value_counts(dropna = False) \
      .reset_index(drop = False)
    col_vals.columns = ['value', 'cnt']  
    col_vals['pcnt'] = 100 * col_vals.cnt / np.sum(col_vals.cnt)
    col_vals = col_vals.sort_values(['pcnt'], ascending = False)
    col_vals = col_vals[['value', 'pcnt', 'cnt']]
    levels_list.append(col_vals)
  # number of unique values per column
  out['cnt'] = [x.shape[0] for x in levels_list]
  out['common'] = [x.value[0] for x in levels_list]
  out['common_pcnt'] = [x.pcnt[0] for x in levels_list]
  out['levels'] = levels_list
  out = out \
    .sort_values('col_name') \
    .reset_index(drop = True)
  # subclass output, adds plot methods
  out = inspect_object(out, my_attr = 'inspect_cat')
  return out  
