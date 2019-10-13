

def show_plot(df) :
  type_types = 'inspect_cat', 'inspect_cor', 'inspect_imb', 'inspect_na'\
                   'inspect_num', 'inspect_mem', 'inspect_types'
  if df.type.isin(type_types) :
    print('sshs')
