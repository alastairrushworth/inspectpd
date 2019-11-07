import pandas as pd
import numpy as np
import plotnine as p9

def plot_na(df) :
  x = df.copy()
  # initialise some extra columns useful for plotting
  x['col_name']   = pd.Categorical(x['col_name'], categories = x['col_name'], ordered = True)
  x['pcnt_print'] = np.round(x.pcnt.values, 1)
  x['pcnt_print_loc_pos'] = (x.pcnt.values) + (np.max(x.pcnt.values))/70
  x['pcnt_print_loc_neg'] = (x.pcnt.values) - (np.max(x.pcnt.values))/70
  # build basic plot
  ggplt = p9.ggplot(x, p9.aes(x = 'col_name', y = 'pcnt', fill = 'col_name'))\
    + p9.geom_bar(stat = 'identity')\
    + p9.guides(fill = False) \
    + p9.ylab('% of values missing') \
    + p9.xlab('') \
    + p9.theme(axis_text_x=p9.element_text(rotation = 45, hjust=1)) 
  # add text labels to the highest bars
  y1 = x.copy()[x.pcnt > 0.3 * np.max(x.pcnt)]
  ggplt = ggplt + \
    p9.geom_text(p9.aes(x = 'col_name', y = 'pcnt_print_loc_neg', label = 'pcnt_print', \
      fill = 'col_name'), inherit_aes = False, data = y1, color = 'white', \
      angle = 90, vjust = 'top')
  # add text labels to the lower bars
  y2 = x.copy()[x.pcnt <= 0.3 * np.max(x.pcnt)]
  ggplt = ggplt + \
    p9.geom_text(p9.aes(x = 'col_name', y = 'pcnt_print_loc_pos', label = 'pcnt_print', \
      fill = 'col_name'), inherit_aes = False, data = y2, color = 'gray', \
      angle = 90, vjust = 'bottom')  
  # return the ggplot object
  return ggplt
