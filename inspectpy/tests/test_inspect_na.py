import inspectdf
import pandas as pd

starwars = pd.read_csv('starwars.csv')

def test_na_df() :
  """
        Test that it can sum a list of integers
  """
  # number of rows equals number of columns of input
  assert starwars.inspect_na().shape[0] == starwars.shape[1]
  
