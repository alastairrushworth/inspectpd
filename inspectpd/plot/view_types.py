import pandas as pd
import numpy as np
import plotnine as p9
from inspectpd.plot.utils import text_sizer, check_summary

def view_types(df) :
  check_summary(df)
  x = df.copy()

  # code on the backburner until plotnine as coord_polar....
  # columns_layout = xx \
  #     .explode('col_name') \
  #     .drop(columns = ['cnt', 'pcnt']) \
  #     .assign(ones = 1) \
  #     .assign(tops = lambda x : np.cumsum(x.ones) / x.ones.sum()) \
  #     .assign(bottoms = lambda x : [0] + x.tops[:-1].tolist()) \
  #     .assign(label_pos = lambda x : (x.tops + x.bottoms) / 2) \
  #     .assign(text_just  = lambda x : ['right' if y > 0.5 else 'left' for y in x.label_pos]) \
  #     .assign(text_rotn = lambda x : [-1 if y > 0.5 else 1 for y in x.label_pos]) \
  #     .assign(text_rotn = lambda x : (x.text_rotn * 90) - (x.label_pos * 360))
  # types_layout = columns_layout \
  #     .groupby('type') \
  #     .size() \
  #     .sort_values(ascending = False) \
  #     .reset_index(drop = False) \
  #     .rename(columns = {0 : 'n'}) \
  #     .assign(tops = lambda x : np.cumsum(x.n) / x.n.sum()) \
  #     .assign(bottoms = lambda x : [0] + x.tops[:-1].tolist()) \
  #     .assign(label_pos = lambda x : (x.tops + x.bottoms) / 2) \
  #     .assign(text_just  = lambda x : ['right' if y > 0.5 else 'left' for y in x.label_pos]) \
  #     .assign(text_rotn = lambda x : [-1 if y > 0.5 else 1 for y in x.label_pos]) \
  #     .assign(text_rotn = lambda x : (x.text_rotn * 90) - (x.label_pos * 360))

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
  text_size = text_sizer(x.shape[0])
  y1 = x.copy()[x.cnt > 0.3 * np.max(x.cnt)]
  if y1.shape[0] > 0 :
    ggplt = ggplt + \
      p9.geom_text(
        p9.aes(
          x = 'new_type', y = 'cnt_print_loc_neg', label = 'cnt', \
          fill = 'type'
        ), 
        inherit_aes = False, data = y1, color = 'white', \
        angle = 90, va= 'top', 
        size = text_size
      )
  # add text labels to the lower bars
  y2 = x.copy()[x.pcnt <= 0.3 * np.max(x.cnt)]
  if y2.shape[0] > 0 :
    ggplt = ggplt + \
      p9.geom_text(
        p9.aes(
          x = 'new_type', y = 'cnt_print_loc_pos', label = 'cnt', \
          fill = 'type'
          ), 
        inherit_aes = False, data = y2, color = 'gray', \
        angle = 90, va = 'bottom', 
        size = text_size
      )  
  return ggplt  
