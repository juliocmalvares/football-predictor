import pathlib
import pandas as pd
import json
import numpy as np
from cleaners import dot_spliter_run



def populate_dataframe(data: list) -> pd.DataFrame:
    return pd.DataFrame(data=[[1,2,3], [4,5,6]], columns=['a', 'b', 'c'])
    # df.loc[i] = ['name' + str(i)] + list(randint(10, size=2))

def build():
    # vanilla_data = dot_spliter_run()
    # print(json.dumps(vanilla_data[0], indent=2))
    print(populate_dataframe(1))



build()