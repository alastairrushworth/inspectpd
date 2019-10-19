import pandas as pd
import numpy as np
from inspectpy.inspect_object.inspect_object import inspect_object

# inspect_types  
def inspect_types(df) : 
  # column types in the df
  col_types = df\
    .dtypes\
    .reset_index(drop = False)
  col_types.columns = ['column', 'type']
  # get totals for each type
  out = pd.DataFrame(col_types.type.value_counts())\
    .reset_index(drop = False)
  # get percentage of columns with each type
  out['pcnt'] = 100 * out.type / np.sum(out.type)
  # rename columns
  out = out.rename(columns = {'index' : 'type', 'type' : 'cnt'})
  # get names of columns with each type
  col_list = []
  for j in out.type :
    col_list.append([col_types.column[i] for i, e in enumerate(col_types.type) if e == j])
  # add column names as new column
  out['col_name'] = col_list
  out = out.sort_values('pcnt', ascending = False)
  # subclass output, adds plot methods
  out = inspect_object(out, my_attr = 'inspect_types')
  return out
