import pandas as pd
import numpy as np
import plotnine as p9

def view_cat(df) :
  lvl_list = []
  # add on the feature name to the levels dfs
  for i in range(df.shape[0]) :
    df.levels[i]['feature'] = df.col_name[i]
    alpha = (100 - df.levels[i].pcnt.cumsum()) / 100
    df.levels[i]['alpha'] = 100 * ((alpha - np.min(alpha)) / np.max(alpha - np.min(alpha)))
    lvl_list.append(df.levels[i])
  
  # combine the levels dfs into a single df
  zz = pd.concat(lvl_list)
  
  # create a feature categorical column
  z_feature_order = df.col_name.to_list()
  z_feature_order.reverse()
  zz['feature'] = pd.Categorical(zz['feature'], ordered = False, categories = z_feature_order)
  
  # basic plot object
  gg_out = \
    p9.ggplot(p9.aes(x = 'feature', y = 'pcnt', fill = 'feature', alpha = 'alpha'), data = zz) \
      + p9.geom_col(position = 'stack', color = "black") \
      + p9.guides(fill = False, alpha = False) \
      + p9.coord_flip() + p9.xlab("") + p9.ylab("") \
      + p9.theme(axis_title_y = p9.element_blank(), panel_background = p9.element_blank(), 
        axis_ticks_minor = p9.element_blank(), axis_ticks_major = p9.element_blank(),
        panel_border = p9.element_blank(), panel_grid_major = p9.element_blank(), 
        axis_title_x = p9.element_blank(), axis_text_x = p9.element_blank())
  
  
  # add cumulative percentage to each 
  cum_perc = zz.groupby('feature')['pcnt'].cumsum()
  #zz[zz.feature == 'gender']
  zz = zz.copy()
  zz['cum_perc'] = cum_perc - zz.pcnt.values
  # create na block - heavily filled
  xx_na = zz[zz['value'].isnull()]
  xx_na = xx_na.drop('alpha', axis = 1)
  xx_na['alpha'] = 100
  xx_na = xx_na.reset_index()
  # create empty block - 100% transparent
  xx_empty = xx_na.copy()
  xx_empty = xx_empty.drop(['alpha', 'pcnt'], axis = 1)
  xx_empty['pcnt'] = xx_empty['cum_perc'].values
  xx_empty['alpha'] = 0
  # combine blocks
  xx = pd.concat([xx_empty, xx_na], sort = True)
  # arrange by feature
  xx = xx.sort_values('feature').reset_index(drop = True)
  # add NAs to plot
  gg_out = \
    gg_out\
      + p9.geom_col(data = xx, \
        mapping=p9.aes(x ='feature', y = 'pcnt', alpha = 'alpha'),\
        position='stack', fill = 'gray', 
        color = 'black',\
        inherit_aes=False)
  
  # add text to the plot
  # text location
  zz = zz.assign(text_pos = zz.cum_perc + (zz.pcnt / 2))
  # filter out small units
  zz = zz[zz.pcnt > 15]
  # add text to plot
  gg_out = \
    gg_out \
      + p9.geom_text(data = zz, 
        mapping = p9.aes(x = 'feature', y = 'text_pos', label = 'value'), 
        inherit_aes = False, color = 'white')
        
  return gg_out

