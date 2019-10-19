import pandas as pd
import numpy as np
import sys as sys
from inspectpd.inspect_object.inspect_object import inspect_object

# inspect_mem  
def inspect_mem(df) :
  out = df\
    .memory_usage(index=False, deep=True)\
    .sort_values(ascending = False)\
    .reset_index(drop = False)
  out.columns = ['col_name', 'bytes']
  # add printable size strings
  out = out.assign(size = out['bytes'].apply(format_size))
  # add percentage of total
  out = out.assign(pcnt = 100 * out['bytes'] / out['bytes'].sum())
  # add type attribute to output
  out = inspect_object(out, my_attr = 'inspect_mem')
  return out

# function for making nice printable object sizes
def format_size(num):
    for unit in ['','K','M','G','T','P','E','Z','Y']:
        if num < 1024.0:
            if unit == '':
              return "%3.f %s%s" % (num, unit, 'B')
            else :
              return "%3.2f %s%s" % (num, unit, 'B')
        num /= 1024.0
    
