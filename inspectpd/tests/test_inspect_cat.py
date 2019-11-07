import inspectpd as ipd
import pandas as pd


# ---------------------------------------------
# check correctness of the returned dataframe
# ---------------------------------------------

def test_inspect_cat_column_names() :
  
  # inspections
  i_starwars = ipd.starwars.inspect_cat()
  i_tech = ipd.tech.inspect_cat()
  i_tdf = ipd.tdf.inspect_cat()
  
  # check the column names
  assert i_starwars.columns.tolist() == ['col_name', 'cnt', 'common', 'common_pcnt', 'levels']
  assert i_tech.columns.tolist() == ['col_name', 'cnt', 'common', 'common_pcnt', 'levels']
  assert i_tdf.columns.tolist() == ['col_name', 'cnt', 'common', 'common_pcnt', 'levels']


# ---------------------------------------------
# check NA counts are correct
# ---------------------------------------------

def test_inspect_na_counts() :
  
  # inspections
  i_starwars = ipd.starwars.inspect_cat()
  i_tech = ipd.tech.inspect_cat()
  i_tdf = ipd.tdf.inspect_cat()
  
  # check the column names
  assert i_starwars.cnt.to_list() == [15, 5, 13, 49, 87, 31, 38]
  assert i_tech.cnt.to_list() == [3158, 51]
  assert i_tdf.cnt.to_list() == [15, 58, 63, 39, 24, 14, 38, 106, 63, 48]
