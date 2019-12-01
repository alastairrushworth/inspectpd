import pandas as pd
import numpy as np
from inspectpd.inspect_object.inspect_object import inspect_object

def inspect_imb(df) :
  
  '''
  Summary of the most common levels in categorical columns
  
  Parameters
  ----------
  
  df: A pandas dataframe.
  
  Returns  
  ----------
  
  A pandas dataframe with columns:
    + col_name: object
      column of strings containing column names of df.
    + value: object
      column of strings containing the most common categorical level 
      in each column of df.
    + cnt: int64 
      the number of occurrences of the most common categorical level 
      in each column of df1.
    + pcnt: float64
      the relative frequency of each column's most common categorical 
      level expressed as a percentage.
  '''
  
  df_cat = df.select_dtypes(['category', 'object'])
  # new df with columns names as first col
  out = pd.DataFrame(df_cat.columns, columns = ['col_name'])
  # tabulate values in each column
  levels_list = []
  for col in df_cat.columns :
    col_vals = df_cat[col] \
      .value_counts() \
      .reset_index(drop = False)
    col_vals.columns = ['value', 'cnt'] 
    col_vals['pcnt'] = 100 * col_vals.cnt / np.sum(col_vals.cnt)
    col_vals = col_vals.sort_values(['pcnt'], ascending = False)
    col_vals = col_vals[['value', 'pcnt', 'cnt']]
    levels_list.append(col_vals)
  # number of unique values per column
  out['value'] = [x.value[0] for x in levels_list]
  out['cnt'] = [x.cnt[0] for x in levels_list]
  out['pcnt'] = [x.pcnt[0] for x in levels_list]
  out = out\
    .sort_values('pcnt', ascending = False)\
    .reset_index(drop = True)
  # subclass output, adds plot methods
  out = inspect_object(out, my_attr = 'inspect_imb')
  return out
