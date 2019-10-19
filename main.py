#call("pip3 list --outdated --format=freeze | grep -v '^\-e' | cut -d = -f 1  | xargs -n1 pip3 install -U")
# --> someway to display lists better in printed output
# --> dtypes misses lists?
# --> check num plot options - rows / columns
# --> change string interbals in hist to tuple / list
# above for inspectdf too
# package tasks
# --> bundle data for examples??
# --> tests for each of the 7 functions - compare to R pkg
# --> overall readme
# --> docstrings

# do an EDA kernel on kaggle when finished

import numpy as np
import pandas as pd
import inspectpd
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
# inspect_num
starwars.inspect_num().show_plot()




# also add bytes / size columns to inspect_mem
# build a new data set for both packages.  male / female cyclists?
# --> turned pro age, retired age, career protour wins, weight, height
# --> total wins, uci rankings, cyclist type, number of teams



























# 
# starwars.inspect_num()
# starwars.inspect_cor()
# starwars.inspect_cat()





