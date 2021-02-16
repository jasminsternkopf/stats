import pandas as pd

from typing import TypeVar, Dict, List


_T = TypeVar('_T')#_T ist float oder int

def get_duration_stats(data_total: Dict[str, List[_T]], data_trn: Dict[str, List[_T]], data_val: Dict[str, List[_T]], data_tst: Dict[str, List[_T]], data_rst: Dict[str, List[_T]]) -> pd.DataFrame:
  pass

def get_duration_df(data_trn: Dict[str, List[_T]], data_val: Dict[str, List[_T]], data_tst: Dict[str, List[_T]], data_rst: Dict[str, List[_T]]) -> pd.DataFrame:
  meta_dataset = get_meta_dict(data_trn, data_val, data_tst, data_rst)
  cols_of_df = get_duration_sums_for_every_speaker_for_all_sets(meta_dataset)#.values())
  print(type(cols_of_df))
  #cols_of_df.insert(0, list(meta_dataset.keys()))
  df=pd.DataFrame(cols_of_df)
  #df['SPEAKER']=list(meta_dataset.keys())
  #df['TRN']=cols_of_df[]
  #df = pd.DataFrame(cols_of_df, columns=['SPEAKER', 'TRN', 'VAL', 'TST', 'RST'])
  return df


def get_duration_sums_for_every_speaker_for_all_sets(dataset: Dict[str, List[List[_T]]]):
  all_duration_sums = [get_duration_sums_for_one_speaker_for_all_sets(speaker,dataset[speaker]) for speaker in dataset.keys()]
  return all_duration_sums

def get_duration_sums_for_one_speaker_for_all_sets(speaker,durations_list: List[List[_T]]):
  duration_sums = [sum(durations) for durations in durations_list]
  duration_sums.insert(0, speaker)
  return duration_sums

# def get_duration_sums_for_every_speaker_for_all_sets(dataset: Dict[str, List[List[_T]]]):
#   all_duration_sums = {speaker: get_duration_sums_for_one_speaker_for_all_sets(dataset[speaker]) for speaker in dataset.keys()}
#   return all_duration_sums

# def get_duration_sums_for_one_speaker_for_all_sets(durations_list: List[List[_T]]):
#   duration_sums = [sum(durations) for durations in durations_list]
#   return duration_sums



# def get_duration_sums_for_every_speaker_for_all_sets(data_trn: Dict[str, List[_T]], data_val: Dict[str, List[_T]], data_tst: Dict[str, List[_T]], data_rst: Dict[str, List[_T]]) -> List[List[_T]]:
#   all_durations = [get_duration_sums_for_every_speaker_for_one_set(dataset) for dataset in [data_trn, data_val, data_tst, data_rst]]
#   all_durations.append(sum(all_durations))
#   return all_durations

# def get_duration_sums_for_every_speaker_for_one_set(dataset: Dict[str, List[_T]]) ->List[_T]:
#   durations = [sum(times) for times in dataset.values()]
#   return durations
  
#def get_duration_df(data_trn: Dict[str, List[_T]], data_tst: Dict[str, List[_T]], data_val: Dict[str, List[_T]], data_rst: Dict[str, List[_T]]) -> pd.DataFrame:
  pass

def get_meta_dict(data_trn: Dict[str, List[_T]], data_val: Dict[str, List[_T]], data_tst: Dict[str, List[_T]], data_rst: Dict[str, List[_T]]) -> Dict[str, List[List[_T]]]:
  #keylists = {dataset.keys() for dataset in [data_trn, data_tst, data_val, data_rst]}
  #all_keys = {key for key in keylist for keylist in keylists}
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