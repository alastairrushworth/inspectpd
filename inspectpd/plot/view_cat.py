import pandas as pd
import numpy as np
import plotnine as p9

def view_cat(df, high_cardinality = 0) :
  # extract the level frequencies from the inspect_cat df
  levels_list = [x for x in df.levels]
  # loop over, add extra columns
  for i in range(len(levels_list)) :
    # put NaNs at the top of the level-list and rename to 'nan'
    levels_list[i] = put_nan_at_top(levels_list[i])
    # merge high cardinalities, if required
    if high_cardinality > 0 :
      levels_list[i] = merge_high_cardinality(levels_list[i], high_cardinality)
    # append feature name as new column
    levels_list[i]['feature'] = df.col_name[i]
    # add alpha shading column, fn of frequency
    alpha = (100 - df.levels[i].pcnt.cumsum()) / 100
    levels_list[i]['alpha'] = 100 * ((alpha - np.min(alpha)) / np.max(alpha - np.min(alpha)))
  # combine the levels into a single df
  zz = pd.concat(levels_list).reset_index(drop = True)
  # coerce feature columns to categorical, ensure ordering is same as in inspect_cat df
  z_feature_order = df.col_name.to_list()
  z_feature_order.reverse()
  zz['feature'] = pd.Categorical(zz['feature'], ordered = False, categories = z_feature_order)
  # add cumulative percentage column
  cum_perc = zz.groupby('feature')['pcnt'].cumsum()
  zz['cum_perc'] = cum_perc - zz.pcnt.values
  # if any missing alphas, make 100
  zz = zz.assign(alpha = zz.alpha.fillna(100.0))
  # basic plot object
  gg_out = \
    p9.ggplot(p9.aes(x = 'feature', y = 'pcnt', fill = 'feature', alpha = 'alpha'), data = zz) \
      + p9.geom_col(position = 'stack', color = "black") \
      + p9.guides(fill = False, alpha = False) \
      + p9.coord_flip() + p9.xlab("") + p9.ylab("") \
      + p9.theme( 
        axis_title_y = p9.element_blank(), panel_background = p9.element_blank(), 
        axis_ticks_minor = p9.element_blank(), axis_ticks_major = p9.element_blank(),
        panel_border = p9.element_blank(), panel_grid_major = p9.element_blank(), 
        axis_title_x = p9.element_blank(), axis_text_x = p9.element_blank()
        )
  
  # color NaNs with gray fill, if there are any
  null_items = zz[zz['value'] == 'nan']
  if null_items.shape[0] > 0 :
    gg_out = gg_out + color_subset(null_items, 'gray', right = False)
  # color high_cardinality with purple fill
  hc_items = zz[zz['value'] == 'High cardinality']
  if (high_cardinality > 0) & (hc_items.shape[0] > 0) :
    gg_out = gg_out + color_subset(hc_items, 'purple')
  # add text to the plot
  # text location
  zz = zz.assign(value = zz.value.astype(object).fillna('_nan'))
  zz = zz.assign(text_pos = zz.cum_perc + (zz.pcnt / 2))
  # filter out small units
  zz = zz[zz.pcnt > 15].reset_index(drop = True)
  if zz.shape[0] > 0 :
    # add text to plot
    gg_out = \
      gg_out \
        + p9.geom_text(
          data = zz, 
          mapping = p9.aes(x = 'feature', y = 'text_pos', label = 'value'), 
          inherit_aes = False, color = 'white'
        )
  return gg_out

# function to combine high cardinality feature values into a single pooled value
def merge_high_cardinality(z, card_thresh) :
  _z = z.copy()
  z_high_card = _z.query('(cnt <= @card_thresh) & (value != "nan")')
  z_high_card = \
      pd.DataFrame(
          {
              'pcnt' : z_high_card.pcnt.sum(), 
              'cnt'  : z_high_card.cnt.sum(),
              'value' : 'High cardinality'
          }, 
          index = [0]
      )            
  z_low_card = _z.query('(cnt > @card_thresh) | (value == "nan")') 
  z_combined = \
      pd.concat([z_low_card, z_high_card]) \
          .drop(columns = 'cnt')
  return z_combined

# put NaNs at top
def put_nan_at_top(z) :
  _z = z.copy()
  z_nan = _z.query('value.isna()')
  if z_nan.shape[0] > 0:
    z_nan = \
        pd.DataFrame(
            {
                'pcnt' : z_nan.pcnt.sum(), 
                'cnt'  : z_nan.cnt.sum(),
                'value' : 'nan'
            }, 
            index = [0]
        )    
  else :
    z_nan = \
        pd.DataFrame(
            {
                'pcnt' : 0.0, 
                'cnt'  : 0,
                'value' : 'nan'
            }, 
            index = [0]
        )  
  z_not_nan = _z.query('~value.isna()') 
  z_combined = pd.concat([z_nan, z_not_nan])
  return z_combined

# function to create color layers for subsets of the inspect_cat.view
def color_subset(subset_df, fill_color, right = True) :
  # create fill block, alpha 100
  subset_df = subset_df.assign(alpha = 100).reset_index()
  # create empty block - alpha transparent
  xx_empty = subset_df.copy()
  xx_empty = xx_empty.drop(['alpha', 'cum_perc'], axis = 1)
  xx_empty['pcnt'] = 100 - xx_empty['pcnt'].values
  xx_empty['alpha'] = 0
  # combine blocks
  xx = pd.concat([xx_empty, subset_df], sort = True)
  # arrange by feature
  xx = xx.sort_values(['feature', 'alpha'], ascending=right).reset_index(drop = True)
  # print(xx)
  # create plot layer
  subset_layer = p9.geom_col(
        data = xx, 
        mapping = p9.aes(x = 'feature', y = 'pcnt', alpha = 'alpha'), 
        position = 'stack', 
        fill = fill_color, 
        color = 'black',
        inherit_aes=False
        )
  return subset_layer