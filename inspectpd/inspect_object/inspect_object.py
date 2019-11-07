import pandas as pd
import numpy as np
from inspectpd.plot.plot_cat import plot_cat
from inspectpd.plot.plot_na import plot_na
from inspectpd.plot.plot_imb import plot_imb
from inspectpd.plot.plot_types import plot_types
from inspectpd.plot.plot_mem import plot_mem
from inspectpd.plot.plot_num import plot_num

# define a subclass with extra methods
class inspect_object(pd.DataFrame):
    # This class variable tells Pandas the name of the attributes
    # that are to be ported over to derivative DataFrames.  There
    # is a method named `__finalize__` that grabs these attributes
    # and assigns them to newly created `SomeData`
    _metadata = ['my_attr']
    @property
    def _constructor(self):
        def _c(*args, **kwargs):
            return inspect_object(*args, **kwargs).__finalize__(self)
        return _c
    def __init__(self, *args, **kwargs):
        # grab the keyword argument that is supposed to be my_attr
        self.my_attr = kwargs.pop('my_attr', None)
        super().__init__(*args, **kwargs)
    def show_plot(self):
        print(self.my_attr)
        # pick appropropriate plotting function based on my_attr
        if self.my_attr == 'inspect_cat' :
          out_plot = plot_cat(self)
        if self.my_attr == 'inspect_na' :
          out_plot = plot_na(self)
        if self.my_attr == 'inspect_imb' :
          out_plot = plot_imb(self)
        if self.my_attr == 'inspect_types' :
          out_plot = plot_types(self)
        if self.my_attr == 'inspect_mem' :
          out_plot = plot_mem(self)
        if self.my_attr == 'inspect_num' :
          out_plot = plot_num(self)
        return out_plot
