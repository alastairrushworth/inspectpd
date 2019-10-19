#call("pip3 list --outdated --format=freeze | grep -v '^\-e' | cut -d = -f 1  | xargs -n1 pip3 install -U")

# --> dtypes misses lists?

# plots complete
# --> inspect_na
# --> inspect_imb
# --> inspect_types
# --> inspect_mem

# package tasks
# --> bundle data for examples??
# --> tests for each of the 7 functions - compare to R pkg
# --> overall readme
# --> docstrings

# do an EDA kernel on kaggle when finished

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import inspectpy
import plotnine as p9

starwars = pd.read_csv('starwars.csv').drop('Unnamed: 0', axis = 1)






# inspect_mem
starwars.inspect_mem().show_plot()
# inspect_imb
starwars.inspect_imb().show_plot()
# inspect_na
starwars.inspect_na().show_plot()
# inspect_types
starwars.inspect_types().show_plot()








starwars.inspect_num()
starwars.inspect_cor()
starwars.inspect_types()
starwars.inspect_mem()
starwars.inspect_cat()
starwars.inspect_imb()




