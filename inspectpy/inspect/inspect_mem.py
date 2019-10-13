import pandas as pd
import numpy as np
import sys as sys

# inspect_mem  
def inspect_mem(df) :
  out = pd.DataFrame(df.columns, columns = ['col_name'])
  size = [sys.getsizeof(df[x]) for x in out.col_name]
  out['size'] = size
  out['pcnt'] = 100 * out['size'] / np.sum(out['size'])
  out = out.sort_values('pcnt', ascending = False)
  # add type attribute to output
  out.type = 'inspect_mem'
  return out
