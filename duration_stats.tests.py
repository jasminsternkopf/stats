from numpy.core.fromnumeric import mean
from duration_stats import *

import pandas as pd

TRAIN = {"a": [1,2,3], "b": [3,4], "d": [1,3,4]}
VAL = {"a": [1,1], "b": [2,1], "c": [1]}
TEST = {"b":[3,5], "c": [7]}
REST = {"d": [4,5]}
TOTAL={"a": [1,2,3,1,1], "b": [3,4,2,1,3,5], "c":[1,7], "d": [1,3,4,4,5]}

meta = get_meta_dict(TRAIN, VAL, TEST, REST,TOTAL)
print(meta)

full=get_duration_stats(TOTAL, TRAIN, VAL, TEST, REST)
print(full.head())

# df = get_duration_df(meta)
# print(df.head())
# reldf = get_rel_duration_df(df)
# print(reldf.head())
# mindf=get_min_df(meta)
# print(mindf.head())
# maxdf=get_max_df(meta)
# print(maxdf.head())
# meandf=get_mean_df(meta)
# print(meandf.head())

# k=TRAIN.keys()
# print(type(k))
# kk=list(k)
# print(type(kk))
# kk.sort()
# print(kk)