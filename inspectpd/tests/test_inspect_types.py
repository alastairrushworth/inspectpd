import inspectdf
import pandas as pd
starwars = pd.read_csv('starwars.csv')

def test_na_df() :
  # number of rows equals number of columns of input
  assert starwars.inspect_na().shape[0] == starwars.shape[1], "some text"
  
