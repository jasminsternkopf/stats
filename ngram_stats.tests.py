import unittest

TRAIN = [["q","b","a"],["a","a"],["b"]]
VAL=[["a","a"],["b"]]
TEST= [["q","b","a"],["c","d"],["b"]]
REST = [["q","b","a"],["a","c"],[2,"a"]]
SYMBOLS = ["a","b","c","d","q"]

from ngram_stats import *

class UnitTests(unittest.TestCase):

    def test_get_occs_of_symb_in_one_set(self):
        double_list = [["q","b","a"],["a","a"],["b"]]
        res = get_occs_of_symb_in_one_set("a", double_list)

        self.assertEqual(res, 3)

    def test_get_occs_for_all_sets(self):
        res = get_occs_for_all_sets("a", TRAIN, VAL, TEST, REST)

        self.assertEqual(len(res), 5)
        self.assertEqual(res[0],3)
        self.assertEqual(res[1],2)
        self.assertEqual(res[2],1)
        self.assertEqual(res[3],3)
        self.assertEqual(res[4],3+2+1+3)


    def test_get_relative_occs_for_all_sets(self):
        pass

    def test_get_total_numbers_of_symbols_for_all_sets(self):
        res = get_total_numbers_of_symbols_for_all_sets(TRAIN, VAL, TEST, REST)

        self.assertEqual(len(res), 5)
        self.assertEqual(res[0],6)
        self.assertEqual(res[1],3)
        self.assertEqual(res[2],6)
        self.assertEqual(res[3],7)
        self.assertEqual(res[4],6+3+6+7)

    def test_get_dists_among_other_symbols(self):
        occs = [3,2,1,3,9]
        total_symbs = [6,3,6,7,22]
        res = get_dists_among_other_symbols(occs, total_symbs)

        self.assertEqual(len(res),5)
        self.assertAlmostEqual(res[0],0.5*100)
        self.assertAlmostEqual(res[1],2/3*100)
        self.assertAlmostEqual(res[2],1/6*100)
        self.assertAlmostEqual(res[3],3/7*100)
        self.assertAlmostEqual(res[4],9/22*100)

    def test_get_utter_occs_of_symbol_in_one_set(self):
        res = get_utter_occs_of_symbol_in_one_set("a", TRAIN)

        self.assertEqual(res, 2)

    def test_get_utter_occs_for_all_sets(self):
        res=get_utter_occs_for_all_sets("a",TRAIN,VAL,TEST,REST)

        self.assertEqual(len(res),5)
        self.assertEqual(res[0],2)
        self.assertEqual(res[1],1)
        self.assertEqual(res[2],1)
        self.assertEqual(res[3],3)
        self.assertEqual(res[4],7)

    def test_get_relative_utter_occs_for_all_sets(self):
        utter_occs = [2,1,1,3,7]
        res = get_relative_utter_occs_for_all_sets(utter_occs)

        self.assertEqual(len(res),4)
        self.assertAlmostEqual(res[0],2/7*100)
        self.assertAlmostEqual(res[1],1/7*100)
        self.assertAlmostEqual(res[2],1/7*100)
        self.assertAlmostEqual(res[3],3/7*100)
        


if __name__ == '__main__':
  suite = unittest.TestLoader().loadTestsFromTestCase(UnitTests)
  unittest.TextTestRunner(verbosity=2).run(suite)

  occ_df = get_occ_df_of_all_symbols(SYMBOLS, TRAIN, VAL, TEST, REST)
  #print(occ_df.head())

  rel_occ_df = get_rel_occ_df_of_all_symbols(occ_df)
  #print(rel_occ_df.head())

  dist_df = get_dist_among_other_symbols_df_of_all_symbols(occ_df, TRAIN, VAL, TEST, REST)
  #print(dist_df.head())

  utter_occ_df = get_utter_occ_df_of_all_symbols(SYMBOLS, TRAIN, VAL, TEST, REST)
  #print(utter_occ_df.head())

  rel_utter_occ_df= get_rel_utter_occ_df_of_all_symbols(utter_occ_df)
  #print(rel_utter_occ_df.head())

  full_df=get_ngram_stats(SYMBOLS, TRAIN, VAL, TEST, REST)
  print(full_df.head())