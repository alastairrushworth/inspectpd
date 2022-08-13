import pandas as pd
from inspectpd.inspect_object.inspect_object import inspect_object

def inspect_num(df) :
  '''
  Summary and comparison of numeric columns
  
  Parameters
  ----------
  
  df: A pandas dataframe.
  
  
  Returns  
  ----------
  
  A pandas dataframe with columns:
    + col_name: object
      column of strings containing column names of df
    + min, q1, median, mean, q3, max and sd: float64
      the minimum, lower quartile, median, mean, upper quartile, 
      maximum and standard deviation for each numeric column.
    + pcnt_na: float64
      the percentage of each numeric feature that is missing
    + hist: object
      a list of tables containing the relative frequency of values
      falling in bins determined by a set of breakpoints.
      
  '''
  df_num = df.select_dtypes('double')
  # construct output dataframe
  out = pd.DataFrame(df_num.columns, columns = ['col_name'])
  # get numerical summaries
  out['min'] = df_num.min().values
  out['q1']  = df_num.quantile(0.25).values
  out['median'] = df_num.median().values
  out['mean'] = df_num.mean().values
  out['q3']  = df_num.quantile(0.75).values
  out['max'] = df_num.max().values
  out['sd'] = df_num.std().values
  out['pcnt_na'] = df_num.isnull().mean().values * 100
  # add histograms to each row of out
  # name the column hist
  hist_list = []
  for num_col in df_num.columns :
    zbins = pd.DataFrame(pd.cut(df_num[num_col], bins = 10).value_counts(num_col))
    zbins = zbins.reset_index(drop = False)
    zbins.columns = ['value', 'prop']
    zbins.sort_values('value')
    hist_list.append(zbins)
  # append the histogram lists as a new column
  out['hist'] = hist_list
  # subclass output, adds plot methods
  out = inspect_object(out, my_attr = 'inspect_num')
  return out
