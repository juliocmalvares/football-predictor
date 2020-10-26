import pathlib
import pandas as pd
import json
import numpy as np
from cleaners import dot_spliter_run


def populate_dataframe() -> pd.DataFrame:
    data_frame = pd.DataFrame(columns=['team',
                                       'date',
                                       'title',
                                       'author',
                                       'text',
                                       'comments',
                                       'url',
                                       'phrases',
                                       'comments_phrases',
                                       ])
    data = dot_spliter_run()
    print("[LOG] Building DataFrame from pandas")
    for i in range(len(data)):
        aux = [data[i]['time'], data[i]['date'], data[i]['title'], data[i]['author'], data[i]['text'],
               data[i]['comments'], data[i]['url'], data[i]['phrases'], data[i]['comments_phrases']]
        data_frame.loc[i] = aux
    return data_frame
    """
        arrumar os tipos, datas
    """

def build():
    df = populate_dataframe()
    print(df.head())

build()
