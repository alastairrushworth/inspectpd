import inspectpd as ipd
import pandas as pd

# ---------------------------------------------
# check correctness of the returned dataframe
# ---------------------------------------------

def test_inspect_types_column_names() :
  
  # inspections
  i_starwars = ipd.starwars.inspect_types()
  i_tdf = ipd.tdf.inspect_types()
  
  # check the column names
  assert i_starwars.columns.tolist() == ['type', 'cnt', 'pcnt', 'col_name'], "Starwars inspect_types df ok"
  assert i_tdf.columns.tolist() == ['type', 'cnt', 'pcnt', 'col_name'], "TDF inspect_types df ok"


# ---------------------------------------------
# check all columns have been summarised
# ---------------------------------------------

def test_inspect_types_columns_summarised() :
  
  # inspections
  i_starwars = ipd.starwars.inspect_types()
  i_tdf = ipd.tdf.inspect_types()

  # check that cnt sums to df.shape[1]
  assert i_starwars.cnt.sum() == ipd.starwars.shape[1]
  assert i_tdf.cnt.sum() == ipd.tdf.shape[1]
