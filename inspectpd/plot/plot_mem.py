import pandas as pd
import numpy as np
import plotnine as p9

def plot_mem(df) :
  x = df.copy()
  # initialise some extra columns useful for plotting
  x['new_cols'] = [str(i) for i in x['col_name']]
  x['new_cols']   = pd.Categorical(x['new_cols'], categories = x['new_cols'], ordered = True)
  x['cnt_print_loc_pos'] = (x.pcnt.values) + (np.max(x.pcnt.values))/70
  x['cnt_print_loc_neg'] = (x.pcnt.values) - (np.max(x.pcnt.values))/70
  # build basic plot
  ggplt  = p9.ggplot(x, p9.aes(x = 'new_cols', y = 'pcnt', fill = 'new_cols')) \
    + p9.geom_bar(stat = 'identity') \
    + p9.guides(fill = False) \
    + p9.ylab('% of total size') \
    + p9.xlab('') \
    + p9.theme(axis_text_x=p9.element_text(rotation = 45, hjust=1)) 
    
  # add text labels to the highest bars
  y1 = x.copy()[x.pcnt > 0.3 * np.max(x.pcnt)]
  ggplt = ggplt + \
    p9.geom_text(p9.aes(x = 'new_cols', y = 'cnt_print_loc_neg', label = 'size', \
      fill = 'col_name'), inherit_aes = False, data = y1, color = 'white', \
      angle = 90, vjust = 'top')
  # add text labels to the lower bars
  y2 = x.copy()[x.pcnt <= 0.3 * np.max(x.pcnt)]
  ggplt = ggplt + \
    p9.geom_text(p9.aes(x = 'new_cols', y = 'cnt_print_loc_pos', label = 'size', \
      fill = 'col_name'), inherit_aes = False, data = y2, color = 'gray', \
      angle = 90, vjust = 'bottom')  
  return ggplt    
