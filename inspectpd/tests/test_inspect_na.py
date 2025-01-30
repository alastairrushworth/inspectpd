import inspectpd as ipd
import pandas as pd


# ---------------------------------------------
# check correctness of the returned dataframe
# ---------------------------------------------

def test_inspect_na_column_names() :
  
  # inspections
  i_starwars = ipd.starwars.inspect_na()
  i_tdf = ipd.tdf.inspect_na()
  
  # check the column names
  assert i_starwars.columns.tolist() == ['col_name', 'cnt', 'pcnt'], "Starwars inspect na df ok"
  assert i_tdf.columns.tolist() == ['col_name', 'cnt', 'pcnt'], "TDF inspect na df ok"


# ---------------------------------------------
# check NA counts are correct
# ---------------------------------------------

def test_inspect_na_counts() :
  
  # inspections
  i_starwars = ipd.starwars.inspect_na()
  i_tdf = ipd.tdf.inspect_na()
  
  # check the column names
  assert i_starwars.cnt.to_list() == [44, 28, 10, 6, 5, 5, 3, 0, 0, 0]
  assert i_tdf.cnt.to_list() == [60, 50, 40, 39, 32, 8, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
