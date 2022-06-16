import pandas as pd
from inspectpd.inspect_object.inspect_object import inspect_object

# inspect_na
def inspect_na(df) :
  '''
  Summary of the rate of missingness across dataframe columns
  
  Parameters
  ----------
  
  df: A pandas dataframe.
  
  Returns  
  ----------
  
  A pandas dataframe with columns:
    + col_name: object
      column of strings containing column names of df
    + cnt: int64
      integer column containing the number of missing values by column.
    + pcnt: float64
      the percentage of records in each column that is missing.
  '''
  
  df_null = df.isnull()
  # number of nulls
  df_nnl  = df_null\
    .sum() \
    .reset_index(drop = False) \
    .rename(columns = {'index' : 'col_name', 0 :  'cnt'})
  # proportion of nulls
  df_mnl = df_null\
    .mean() \
    .reset_index(drop = False) \
    .rename(columns = {'index' : 'col_name', 0 : 'pcnt'})
  # convert proportion to percentage
  df_mnl = df_mnl.assign(pcnt = df_mnl.pcnt * 100)
  # combine null summary into single df
  out = df_nnl.merge(df_mnl, on = 'col_name', how = 'left')
  out = out \
    .sort_values('pcnt', ascending = False) \
    .reset_index(drop = True)
  # subclass output, adds plot methods
  out = inspect_object(out, my_attr = 'inspect_na')
  return out
