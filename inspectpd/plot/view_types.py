import pandas as pd
import numpy as np
import plotnine as p9

def view_types(df) :
  x = df.copy()
  # initialise some extra columns useful for plotting
  x['new_type'] = [str(i) for i in x['type']]
  x['new_type']   = pd.Categorical(x['new_type'], categories = x['new_type'], ordered = True)
  x['cnt_print_loc_pos'] = (x.cnt.values) + (np.max(x.cnt.values))/70
  x['cnt_print_loc_neg'] = (x.cnt.values) - (np.max(x.cnt.values))/70
  # build basic plot
  ggplt  = p9.ggplot(x, p9.aes(x = 'new_type', y = 'cnt', fill = 'new_type')) \
    + p9.geom_bar(stat = 'identity') \
    + p9.guides(fill = False) \
    + p9.ylab('Number of columns') \
    + p9.xlab('') \
    + p9.theme(axis_text_x=p9.element_text(rotation = 45, hjust=1)) 
    
  # add text labels to the highest bars
  y1 = x.copy()[x.cnt > 0.3 * np.max(x.cnt)]
  ggplt = ggplt + \
    p9.geom_text(p9.aes(x = 'new_type', y = 'cnt_print_loc_neg', label = 'cnt', \
      fill = 'type'), inherit_aes = False, data = y1, color = 'white', \
      angle = 90, va= 'top')
  # add text labels to the lower bars
  y2 = x.copy()[x.pcnt <= 0.3 * np.max(x.cnt)]
  ggplt = ggplt + \
    p9.geom_text(p9.aes(x = 'new_type', y = 'cnt_print_loc_pos', label = 'cnt', \
      fill = 'type'), inherit_aes = False, data = y2, color = 'gray', \
      angle = 90, va = 'bottom')  
  return ggplt  
