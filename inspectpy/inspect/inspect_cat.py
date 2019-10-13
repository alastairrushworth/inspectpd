import pandas as pd
import numpy as np

# TODO

# inspect_cat  
def inspect_cat(df) :
  # get the string / categorical columns
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
  out['cnt'] = [x.shape[0] for x in levels_list]
  out['common'] = [x.value[0] for x in levels_list]
  out['common_pcnt'] = [x.pcnt[0] for x in levels_list]
  out['levels'] = levels_list
  out = out\
    .sort_values('col_name')\
    .reset_index(drop = True)
  # add type attribute to output
  out.type = 'inspect_cat'
  return out  
