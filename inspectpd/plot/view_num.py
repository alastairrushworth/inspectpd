import pandas as pd
import numpy as np
import plotnine as p9

def view_num(df) :
  if df.shape[0] == 0 :
    raise RuntimeError('No numeric columns to view')
  x = df.copy()
  # add group column to the 
  z = x['hist'].to_list()
  for i in range(len(z)) : 
    z[i]['groups'] = x['col_name'][i] 
  z = pd.concat(z)
  # generate the plot
  ggplt = p9.ggplot(z, p9.aes(x = 'value', y = 'prop', group = 'groups'))\
    + p9.geom_col()\
    + p9.guides(fill = False) \
    + p9.ylab('Proportion') \
    + p9.xlab('') \
    + p9.theme(axis_text_x=p9.element_text(rotation = 45, hjust=1))\
    + p9.facet_wrap(facets = ['groups'], ncol = 3, scales = 'free')
  # return the plot object
  return ggplt
