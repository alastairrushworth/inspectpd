import pandas as pd
import numpy as np
import plotnine as p9

def plot_cor(df) :
  # drop missing correlations
  out = df[~df['corr'].isnull()]
  # add pair column
  out = out.assign(pair = out.col_1 + '&' + out.col_2)
  # add a sign column
  sign = ((out['corr'] > 0).astype('int')).to_list()
  sign = [['Negative', 'Positive'][i] for i in sign]
  out['sign'] = sign
  #out  = out.sort_values('pair', ascending = False).reset_index(drop = True)
  # add ind column
  out['ind'] = [out.shape[0] - i for i in range(out.shape[0])]
  # plot using bands
  ggplt = p9.ggplot(data = out, mapping = p9.aes(x = 'pair', y = 'corr')) \
      + p9.geom_hline(
          yintercept = 0, 
          linetype = "dashed",
          color = "#c2c6cc"
          ) \
      + p9.geom_rect(
          alpha = 0.4,
          xmin = out.ind.values - 0.4, 
          xmax = out.ind.values + 0.4,
          ymin = out.lower.values, 
          ymax = out.upper.values,
          fill = [['b', '#abaeb3'][int(x > 0.05)] for x in out.p_value]
        ) \
      + p9.geom_segment(
          x = out.ind.values - 0.4, 
          y = out['corr'].values, 
          xend = out.ind.values + 0.4, 
          yend = out['corr'].values
        ) \
      + p9.coord_flip() \
      + p9.ylim(np.min(out.lower.values), np.max(out.upper.values)) \
      + p9.labs(x = "", y = "Correlation")
  return ggplt
