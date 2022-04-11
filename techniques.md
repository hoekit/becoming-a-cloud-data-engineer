# Data Techniques

----
### Locate Missing Data
__

import pandas as pd
import numpy as np

data = pd.read_csv('source.csv')

data.isnull()

data.isnull().any()

data.isnull().sum()

..

----
### Locate Duplicates
__

import pandas as pd

data = pd.read_csv("source.csv")

data.duplicated()                                   # Find dups

data.drop_duplicates()                              # Drop dups
..


----
### Use the missingno package
__ https://github.com/ResidentMario/missingno
..


----
#### Standardize casing
__

data['Column_1'] = data['Column_1'].str.lower()
data['Column_2'] = data['Column_2'].str.title()

..

