import pandas as pd
import numpy as np

from typing import TypeVar, Dict, List


_T = TypeVar('_T')

def get_duration_stats(data_total: Dict[str, List[_T]], data_trn: Dict[str, List[_T]], data_val: Dict[str, List[_T]], data_tst: Dict[str, List[_T]], data_rst: Dict[str, List[_T]]) -> pd.DataFrame:
  pass

def get_min_df(meta_dataset) -> pd.DataFrame:
  lines_of_df = get_minimum_durations_for_every_speaker_for_all_sets(meta_dataset)
  df = pd.DataFrame(lines_of_df, columns=['SPEAKER', 'DUR TRN', 'VAL', 'TST', 'RST','TOTAL'])
  return df

def get_minimum_durations_for_every_speaker_for_all_sets(dataset: Dict[str, List[List[_T]]]) -> List[List]:
  sorted_keylist = list(dataset.keys())
  sorted_keylist.sort()
  all_duration_sums = [get_minimum_durations_for_one_speaker_for_all_sets(speaker,dataset[speaker]) for speaker in sorted_keylist]
  return all_duration_sums

def get_minimum_durations_for_one_speaker_for_all_sets(speaker,durations_list: List[List[_T]]) -> List:
  mins = [min(durations) if durations != [0] else "-" for durations in durations_list]
  mins.append(min(mins)) #so that we don't have to compute it for total set
  mins.insert(0, speaker)
  return mins

def get_dist():
  pass

def get_rel_duration_df(durations_df: pd.DataFrame) -> pd.DataFrame:
  df_as_row_wise_array = durations_df.to_numpy()
  df_lines = []
  for row in df_as_row_wise_array:
      rel_durations_list = get_relative_durations_for_all_sets(row[1:])
      rel_durations_list.insert(0, row[0])
      df_lines.append(rel_durations_list)
  df = pd.DataFrame(df_lines, columns = ['SPEAKER','REL_DUR TRN', 'VAL', 'TST', 'RST'])
  return df

def get_relative_durations_for_all_sets(duration_list: List[_T]) -> List[float]:
  rel_durations=100*np.array(duration_list[:-1])/duration_list[-1]
  return rel_durations.tolist()


def get_duration_df(data_trn: Dict[str, List[_T]], data_val: Dict[str, List[_T]], data_tst: Dict[str, List[_T]], data_rst: Dict[str, List[_T]]) -> pd.DataFrame:
  meta_dataset = get_meta_dict(data_trn, data_val, data_tst, data_rst)
  lines_of_df = get_duration_sums_for_every_speaker_for_all_sets(meta_dataset)
  df = pd.DataFrame(lines_of_df, columns=['SPEAKER', 'DUR TRN', 'VAL', 'TST', 'RST','TOTAL'])
  return df

def get_duration_sums_for_every_speaker_for_all_sets(dataset: Dict[str, List[List[_T]]]) -> List[List]:
  sorted_keylist = list(dataset.keys())
  sorted_keylist.sort()
  all_duration_sums = [get_duration_sums_for_one_speaker_for_all_sets(speaker,dataset[speaker]) for speaker in sorted_keylist]
  return all_duration_sums

def get_duration_sums_for_one_speaker_for_all_sets(speaker,durations_list: List[List[_T]]) -> List:
  duration_sums = [sum(durations) for durations in durations_list]
  duration_sums.append(sum(duration_sums)) #so that we don't have to compute it for total set
  duration_sums.insert(0, speaker)
  return duration_sums

def get_meta_dict(data_trn: Dict[str, List[_T]], data_val: Dict[str, List[_T]], data_tst: Dict[str, List[_T]], data_rst: Dict[str, List[_T]]) -> Dict[str, List[List[_T]]]:
  all_keys = {key for key_list in [data_trn.keys(), data_val.keys(), data_tst.keys(), data_rst.keys()] for key in key_list}
  meta_dict = {key: get_duration_values_for_key(key, data_trn, data_val, data_tst, data_rst) for key in all_keys}
  return meta_dict

def get_duration_values_for_key(key: str, data_trn: Dict[str, List[_T]], data_val: Dict[str, List[_T]], data_tst: Dict[str, List[_T]], data_rst: Dict[str, List[_T]]) -> List[_T]:
  values = [duration_or_zero(key, data) for data in [data_trn, data_val, data_tst, data_rst]]
  return values

def duration_or_zero(key: str, data: Dict[str, List[_T]]) -> List[_T]:
  if key in data.keys():
    return data[key]
  return [0]