import pandas as pd
import numpy as np

def inspect_num(df) :
  df_num = df.select_dtypes('double')
  # construct output dataframe
  out = pd.DataFrame(df_num.columns, columns = ['col_name'])
  # get numerical summaries
  out['min'] = df_num.min().values
  out['q1']  = df_num.apply(lambda x : np.nanpercentile(x, q = 0.25), axis = 0).values
  out['median'] = df_num.apply(lambda x : np.nanpercentile(x, q = 0.5), axis = 0).values
  out['q3']  = df_num.apply(lambda x : np.nanpercentile(x, q = 0.75), axis = 0).values
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
  # add type attribute to output
  out.type = 'inspect_num'
  return out
