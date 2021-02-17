from numpy.core.fromnumeric import mean
from numpy.core.numeric import Infinity, NaN
import pandas as pd
import numpy as np

from typing import TypeVar, Dict, List

FIRST_COL = "SPEAKER"
_T = TypeVar('_T')

def get_duration_stats(speakers: List[str], data_trn: Dict[str, List[_T]], data_val: Dict[str, List[_T]], data_tst: Dict[str, List[_T]], data_rst: Dict[str, List[_T]], data_total: Dict[str, List[_T]]) -> pd.DataFrame:
  meta_dataset = get_meta_dict(speakers, data_trn, data_val, data_tst, data_rst, data_total)
  duration_df = get_duration_df(speakers, meta_dataset)
  rel_duration_df = get_rel_duration_df(duration_df)
  dist_df = get_dist_df(duration_df)
  min_df = get_min_df(speakers, meta_dataset)
  max_df = get_max_df(speakers, meta_dataset)
  mean_df = get_mean_df(speakers, meta_dataset)
  full_df = pd.concat([
      duration_df,
      rel_duration_df.loc[:, rel_duration_df.columns != FIRST_COL],
      dist_df.loc[:, dist_df.columns != FIRST_COL],
      min_df.loc[:, min_df.columns != FIRST_COL],
      max_df.loc[:, max_df.columns != FIRST_COL],
      mean_df.loc[:, mean_df.columns != FIRST_COL]
      ],
      axis=1,
      join='inner')
  return full_df


def get_mean_df(speakers: List[str], meta_dataset) -> pd.DataFrame:
  lines_of_df = get_mean_durations_for_every_speaker_for_all_sets(speakers, meta_dataset)
  df = pd.DataFrame(lines_of_df, columns=['SPEAKER', 'MEAN TRN', 'VAL', 'TST', 'RST','TOTAL'])
  last_line = mean_of_df(df)
  last_line.replace(0,"-",inplace=True)
  df=df.append(last_line, ignore_index=True)
  df.iloc[-1,0] ="all"
  return df

def mean_of_df(data: pd.DataFrame) -> pd.Series:
  data_without_hyphen = data.replace("-", NaN)
  means = data_without_hyphen.mean()
  means.replace(NaN, "-", inplace=True)
  return means

def get_mean_durations_for_every_speaker_for_all_sets(speakers: List[str], dataset: Dict[str, List[List[_T]]]) -> List[List]:
  all_means = [get_mean_durations_for_one_speaker_for_all_sets(speaker,dataset[speaker]) for speaker in speakers]
  return all_means

def get_mean_durations_for_one_speaker_for_all_sets(speaker,durations_list: List[List[_T]]) -> List:
  means = [mean(durations) if durations != [0] else "-" for durations in durations_list]
  means.insert(0, speaker)
  return means

def get_max_df(speakers: List[str], meta_dataset) -> pd.DataFrame:
  lines_of_df = get_maximum_durations_for_every_speaker_for_all_sets(speakers, meta_dataset)
  df = pd.DataFrame(lines_of_df, columns=['SPEAKER', 'MAX TRN', 'VAL', 'TST', 'RST','TOTAL'])
  last_line = maximum_of_df(df)
  last_line.replace(0,"-",inplace=True)
  df=df.append(last_line, ignore_index=True)
  df.iloc[-1,0] ="all"
  return df

def maximum_of_df(data: pd.DataFrame) -> pd.Series:
  data_without_hyphen = data.replace("-", 0)
  maxs = data_without_hyphen.max()
  maxs.replace(0, "-", inplace=True)
  return maxs

def get_maximum_durations_for_every_speaker_for_all_sets(speakers: List[str], dataset: Dict[str, List[List[_T]]]) -> List[List]:
  all_maxima = [get_maximum_durations_for_one_speaker_for_all_sets(speaker,dataset[speaker]) for speaker in speakers]
  return all_maxima

def get_maximum_durations_for_one_speaker_for_all_sets(speaker,durations_list: List[List[_T]]) -> List:
  maxs = [max(durations) if durations != [0] else "-" for durations in durations_list]
  maxs.insert(0, speaker)
  return maxs

def get_min_df(speakers: List[str], meta_dataset) -> pd.DataFrame:
  lines_of_df = get_minimum_durations_for_every_speaker_for_all_sets(speakers, meta_dataset)
  df = pd.DataFrame(lines_of_df, columns=['SPEAKER', 'MIN TRN', 'VAL', 'TST', 'RST','TOTAL'])
  last_line = minimum_of_df(df)
  df=df.append(last_line, ignore_index=True)
  df.iloc[-1,0] ="all"
  return df

def minimum_of_df(data: pd.DataFrame) -> pd.Series:
  data_without_hyphen = data.replace("-", Infinity)
  mins = data_without_hyphen.min()
  mins.replace(Infinity, "-", inplace=True)
  return mins

def get_minimum_durations_for_every_speaker_for_all_sets(speakers: List[str], dataset: Dict[str, List[List[_T]]]) -> List[List]:
  all_minima = [get_minimum_durations_for_one_speaker_for_all_sets(speaker,dataset[speaker]) for speaker in speakers]
  return all_minima

def get_minimum_durations_for_one_speaker_for_all_sets(speaker,durations_list: List[List[_T]]) -> List:
  mins = [min(durations) if durations != [0] else "-" for durations in durations_list]
  mins.insert(0, speaker)
  return mins

def get_dist_df(durations_df: pd.DataFrame) -> pd.DataFrame:
  durations_df.replace("-",0,inplace=True)
  df = durations_df.loc[0:len(durations_df.index)-2, durations_df.columns != FIRST_COL].copy()
  df.rename(columns = {"DUR TRN": "DIST TRN"}, inplace = True)
  dataset_lengths = df.sum()
  df = 100* df.div(dataset_lengths)
  df.insert(loc=0, column=FIRST_COL, value = durations_df.loc[0:len(durations_df.index)-2, durations_df.columns==FIRST_COL])
  last_line = df.sum()
  df=df.append(last_line, ignore_index=True)
  df.iloc[-1,0] ="all"
  df.replace(0,"-",inplace=True)
  df.replace(NaN,"-",inplace=True)
  durations_df.replace(0,"-",inplace=True)
  return df

def get_whole_dataset_duration(dataset: Dict[str, List[List[_T]]]) -> _T:
  duration_for_each_speaker = [sum(durations) for durations in list(dataset.values())]
  return sum(duration_for_each_speaker)

def get_rel_duration_df(durations_df: pd.DataFrame) -> pd.DataFrame:
  durations_df.replace("-",0,inplace=True)
  df_as_row_wise_array = durations_df.to_numpy()
  df_lines = []
  for row in df_as_row_wise_array[:-1,:]:
      rel_durations_list = get_relative_durations_for_all_sets(row[1:])
      rel_durations_list.insert(0, row[0])
      df_lines.append(rel_durations_list)
  df = pd.DataFrame(df_lines, columns = ['SPEAKER','REL_DUR TRN', 'VAL', 'TST', 'RST'])
  last_line = df.sum()
  df=df.append(last_line, ignore_index=True)
  df.iloc[-1,0] ="all"
  norm_factor = last_line[1:].sum()/100
  df.iloc[-1, 1:] = df.iloc[-1, 1:].div(norm_factor)
  df.replace(0,"-",inplace=True)
  durations_df.replace(0,"-",inplace=True)
  return df

def get_relative_durations_for_all_sets(duration_list: List[_T]) -> List:
  if duration_list[-1] == 0: #falls ein Sprecher in keinem Set vorkommt
    return [0]*(len(duration_list)-1)
  rel_durations=100*np.array(duration_list[:-1])/duration_list[-1]
  return rel_durations.tolist()


def get_duration_df(speakers: List[str], meta_dataset: Dict[str, List[List[_T]]]) -> pd.DataFrame:
  lines_of_df = get_duration_sums_for_every_speaker_for_all_sets(speakers, meta_dataset)
  df = pd.DataFrame(lines_of_df, columns=['SPEAKER', 'DUR TRN', 'VAL', 'TST', 'RST','TOTAL'])
  last_line = df.sum()
  df=df.append(last_line, ignore_index=True)
  df.iloc[-1,0] ="all"
  df.replace(0,"-",inplace=True)
  return df

def get_duration_sums_for_every_speaker_for_all_sets(speakers: List[str], dataset: Dict[str, List[List[_T]]]) -> List[List]:
  all_duration_sums = [get_duration_sums_for_one_speaker_for_all_sets(speaker,dataset[speaker]) for speaker in speakers]
  return all_duration_sums

def get_duration_sums_for_one_speaker_for_all_sets(speaker,durations_list: List[List[_T]]) -> List:
  duration_sums = [sum(durations) for durations in durations_list]
  duration_sums.insert(0, speaker)
  return duration_sums

def get_meta_dict(speakers: List[str], data_trn: Dict[str, List[_T]], data_val: Dict[str, List[_T]], data_tst: Dict[str, List[_T]], data_rst: Dict[str, List[_T]], data_total: Dict[str, List[_T]]) -> Dict[str, List[List[_T]]]:
  meta_dict = {speaker: get_duration_values_for_key(speaker, data_trn, data_val, data_tst, data_rst, data_total) for speaker in speakers}
  return meta_dict

def get_duration_values_for_key(speaker: str, data_trn: Dict[str, List[_T]], data_val: Dict[str, List[_T]], data_tst: Dict[str, List[_T]], data_rst: Dict[str, List[_T]], data_total: Dict[str, List[_T]]) -> List[_T]:
  values = [duration_or_zero(speaker, data) for data in [data_trn, data_val, data_tst, data_rst, data_total]]
  return values

def duration_or_zero(speaker: str, data: Dict[str, List[_T]]) -> List[_T]:
  if speaker in data.keys():
    return data[speaker]
  return [0]