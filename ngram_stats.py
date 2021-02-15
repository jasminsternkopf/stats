from typing import List, Tuple, TypeVar
import pandas as pd
import numpy as np
from pandas.core.frame import DataFrame

_T = TypeVar('_T')


def get_ngram_stats(symbols: List[_T], data_trn: List[List[_T]], data_val: List[List[_T]], data_tst: List[List[_T]], data_rst: List[List[_T]]) -> pd.DataFrame:
    occ_df = get_occ_df_of_all_symbols(symbols, data_trn, data_val, data_tst, data_rst)
    rel_occ_df = get_rel_occ_df_of_all_symbols(occ_df)
    dist_df = get_dist_among_other_symbols_df_of_all_symbols(occ_df, data_trn, data_val, data_tst, data_rst)
    utter_occ_df = get_utter_occ_df_of_all_symbols(symbols, data_trn, data_val, data_tst, data_rst)
    rel_utter_occ_df=get_rel_utter_occ_df_of_all_symbols(utter_occ_df)
    full_df = pd.concat([
                occ_df,
                rel_occ_df.loc[:, rel_occ_df.columns != "SYMB"],
                dist_df.loc[:, dist_df.columns != "SYMB"],
                utter_occ_df.loc[:, utter_occ_df.columns != "SYMB"],
                rel_utter_occ_df.loc[:, rel_utter_occ_df.columns != "SYMB"]
                ],
                axis=1,
                join='inner')
    return full_df

def get_rel_utter_occ_df_of_all_symbols(utter_occs_df: pd.DataFrame) -> pd.DataFrame:
    df_as_row_wise_array = utter_occs_df.to_numpy()
    df_lines = []
    for row in df_as_row_wise_array:
        rel_utter_occ_list = get_relative_utter_occs_for_all_sets(row[1:])
        rel_utter_occ_list.insert(0, row[0])
        df_lines.append(rel_utter_occ_list)
    df = pd.DataFrame(df_lines, columns = ['SYMB','REL_UTT TRN', 'VAL', 'TST', 'RST'])
    return df

def get_relative_utter_occs_for_all_sets(utter_occs_list: List[int]) -> List[float]:
    relative_utter_occs=100*np.array(utter_occs_list[:-1])/utter_occs_list[-1]
    return relative_utter_occs.tolist()

def get_utter_occ_df_of_all_symbols(symbols: List[_T], data_trn: List[List[_T]], data_val: List[List[_T]], data_tst: List[List[_T]], data_rst: List[List[_T]]) -> pd.DataFrame:
    df_lines = []
    for symb in symbols:
        utter_occ_list = get_utter_occs_for_all_sets(symb, data_trn, data_val, data_tst, data_rst)
        utter_occ_list.insert(0, symb)
        df_lines.append(utter_occ_list)
    df = pd.DataFrame(df_lines, columns = ['SYMB','UTT TRN', 'VAL', 'TST', 'RST', 'TOTAL'])
    return df

def get_utter_occs_for_all_sets(symb: _T, data_trn: List[List[_T]], data_val: List[List[_T]], data_tst: List[List[_T]], data_rst: List[List[_T]]) -> List[int]:
    utter_occs = [get_utter_occs_of_symbol_in_one_set(symb, dataset) for dataset in [data_trn, data_val, data_tst, data_rst]]
    utter_occs.append(sum(utter_occs))
    return utter_occs

def get_utter_occs_of_symbol_in_one_set(symb: _T, dataset: List[List[_T]]) -> int:
    symb_is_in_single_list = [symb in single_list for single_list in dataset]
    return sum(symb_is_in_single_list)

def get_dist_among_other_symbols_df_of_all_symbols(occs_df: pd.DataFrame, data_trn: List[List[_T]], data_val: List[List[_T]], data_tst: List[List[_T]], data_rst: List[List[_T]]) -> pd.DataFrame:
    df_as_row_wise_array = occs_df.to_numpy()
    df_lines = []
    total_symb_numbers = get_total_numbers_of_symbols_for_all_sets(data_trn, data_val, data_tst, data_rst)
    for row in df_as_row_wise_array:
        dist_list = get_dists_among_other_symbols(row[1:], total_symb_numbers)
        dist_list.insert(0, row[0])
        df_lines.append(dist_list)
    df = pd.DataFrame(df_lines, columns = ['SYMB','DIST TRN', 'VAL', 'TST', 'RST', 'TOTAL'])
    return df

def get_dists_among_other_symbols(occs_of_symb: List[int], total_numb_of_symbs: List[int]) -> List[float]:
    dists = np.array(occs_of_symb)/np.array(total_numb_of_symbs)*100
    return dists.tolist()

def get_total_numbers_of_symbols_for_all_sets(data_trn: List[List[_T]], data_val: List[List[_T]], data_tst: List[List[_T]], data_rst: List[List[_T]]) ->List[int]:
    total_symb_numbers = [total_number_of_symbols_in_double_list(dataset) for dataset in [data_trn, data_val, data_tst, data_rst]]
    total_symb_numbers.append(sum(total_symb_numbers))
    return total_symb_numbers

def total_number_of_symbols_in_double_list(double_list: List[List[_T]]) -> int:
    lens_of_single_lists = [len(single_list) for single_list in double_list]
    return sum(lens_of_single_lists)

def get_rel_occ_df_of_all_symbols(occs_df: pd.DataFrame) -> pd.DataFrame:
    df_as_row_wise_array = occs_df.to_numpy()
    df_lines = []
    for row in df_as_row_wise_array:
        rel_occ_list = get_relative_occs_for_all_sets(row[1:])
        rel_occ_list.insert(0, row[0])
        df_lines.append(rel_occ_list)
    df = pd.DataFrame(df_lines, columns = ['SYMB','REL_OCC TRN', 'VAL', 'TST', 'RST'])
    return df

def get_relative_occs_for_all_sets(occs_list: np.array) -> List[float]: #List[int]
    relative_occs=100*np.array(occs_list[:-1])/occs_list[-1]
    return relative_occs.tolist()

def get_occ_df_of_all_symbols(symbols: List[_T], data_trn: List[List[_T]], data_val: List[List[_T]], data_tst: List[List[_T]], data_rst: List[List[_T]]) -> pd.DataFrame:
    df_lines = []
    for symb in symbols:
        occ_list = get_occs_for_all_sets(symb, data_trn, data_val, data_tst, data_rst)
        occ_list.insert(0, symb)
        df_lines.append(occ_list)
    df = pd.DataFrame(df_lines, columns = ['SYMB','OCC TRN', 'VAL', 'TST', 'RST', 'TOTAL'])
    return df
    

def get_occs_for_all_sets(symb: _T, data_trn: List[List[_T]], data_val: List[List[_T]], data_tst: List[List[_T]], data_rst: List[List[_T]]) -> List[int]:
    occs = [get_occs_of_symb_in_one_set(symb, dataset) for dataset in [data_trn, data_val, data_tst, data_rst]]
    occs.append(sum(occs))
    return occs

def get_occs_of_symb_in_one_set(symb: _T, double_list: List[List[_T]]) -> int:
    occs_of_symb_in_lists_of_double_list = [single_list.count(symb) for single_list in double_list]
    return sum(occs_of_symb_in_lists_of_double_list)