from pandas import DataFrame
from inspectpd.plot.view_cat import view_cat
from inspectpd.plot.view_cor import view_cor
from inspectpd.plot.view_na import view_na
from inspectpd.plot.view_imb import view_imb
from inspectpd.plot.view_types import view_types
from inspectpd.plot.view_mem import view_mem
from inspectpd.plot.view_num import view_num

# define a subclass with extra methods
class inspect_object(DataFrame):
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
    def view(self):
        # pick appropropriate plotting function based on my_attr
        if self.my_attr == 'inspect_cat' :
          out_plot = view_cat(self)
        if self.my_attr == 'inspect_cor' :
          out_plot = view_cor(self)
        if self.my_attr == 'inspect_na' :
          out_plot = view_na(self)
        if self.my_attr == 'inspect_imb' :
          out_plot = view_imb(self)
        if self.my_attr == 'inspect_types' :
          out_plot = view_types(self)
        if self.my_attr == 'inspect_mem' :
          out_plot = view_mem(self)
        if self.my_attr == 'inspect_num' :
          out_plot = view_num(self)
        return out_plot
