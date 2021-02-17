from numpy.core.fromnumeric import mean
from duration_stats import *

import pandas as pd

TRAIN = {"a": [1,2,3], "b": [3,4], "d": [1,3,4]}
VAL = {"a": [1,1], "b": [2,1], "c": [1]}
TEST = {"b":[3,5], "c": [7], "f": [1,3]}
REST = {}
#REST = {"d": [4,5]}
#TOTAL={"a": [1,2,3,1,1], "b": [3,4,2,1,3,5], "c":[1,7], "d": [1,3,4,4,5]}
TOTAL={"a": [1,2,3,1,1], "b": [3,4,2,1,3,5], "c":[1,7], "d": [1,3,4], "f": [1,3]}
SPEAKERS = ["a","c","b","d","e","f"]

meta = get_meta_dict(SPEAKERS, TRAIN, VAL, TEST, REST,TOTAL)
#print(meta)

full=get_duration_stats(SPEAKERS, TRAIN, VAL, TEST, REST, TOTAL)
print(full.head(10))

df = get_duration_df(SPEAKERS, meta)
#print(df.head(10))
#d=df.loc[:, df.columns !="SPEAKER"]
#dsum=d.min()
#print(dsum)
#dmin=minimum(d)
#print(dmin)
#print(type(dmin))
#print(df.sum())#["VAL","TST","RST"]
dist = get_dist_df(df)
#print(dist.head(10))
reldf = get_rel_duration_df(df)
#print(reldf.head(10))
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