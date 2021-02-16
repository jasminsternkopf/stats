from duration_stats import *

import pandas as pd

TRAIN = {"a": [1,2,3], "b": [3,4], "d": [1,3,4]}
VAL = {"a": [1,1], "b": [2,1], "c": [1]}
TEST = {"b":[3,5], "c": [7]}
REST = {"d": [4,5]}

meta = get_meta_dict(TRAIN, VAL, TEST, REST)
print(meta)

df = get_duration_df(TRAIN, VAL, TEST, REST)
#print(df)
reldf = get_rel_duration_df(df)
#print(reldf)
mindf=get_min_df(meta)
print(mindf)

# k=TRAIN.keys()
# print(type(k))
# kk=list(k)
# print(type(kk))
# kk.sort()
# print(kk)