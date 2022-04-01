# import inspect_ fns
from .inspect.inspect_types import inspect_types
from .inspect.inspect_na    import inspect_na
from .inspect.inspect_cat   import inspect_cat
from .inspect.inspect_cor   import inspect_cor
from .inspect.inspect_imb   import inspect_imb
from .inspect.inspect_mem   import inspect_mem
from .inspect.inspect_num   import inspect_num


# monkey-patch as methods to pandas
from pandas.core.base import PandasObject
PandasObject.inspect_imb = inspect_imb
PandasObject.inspect_na = inspect_na
PandasObject.inspect_types = inspect_types
PandasObject.inspect_mem = inspect_mem
PandasObject.inspect_cat = inspect_cat
PandasObject.inspect_cor = inspect_cor
PandasObject.inspect_num = inspect_num

# import data
from pandas import read_csv
starwars = read_csv('inspectpd/data/starwars.csv', index_col = 0)
tech = read_csv('inspectpd/data/tech.csv')
tdf = read_csv('inspectpd/data/tdf.csv')
