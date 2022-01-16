import unittest
from unittest.mock import patch
from mock import call
import os

import pandas as pd
from pandas._testing import assert_frame_equal

from loanpy import adapter as ad

path=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))#+r"\data"

class Test1(unittest.TestCase):
    
    def test_launch(self):
        
        substidict_test={'a': 'a, æ','auaɪ': 'æ, u, o, i, e','ndrs': 'n, t, r, s, nt'}
        with open("substidict_test.txt","w",encoding="utf-8") as data:
            data.write(str(substidict_test))
        uralonet_test=pd.DataFrame({"New": ["mɛʃɛ","aːɟ","ɒl"], "Old": ["ɑt͡ʃʲɑ","ɑðʲɜ","ɑlɑ"],"Lan": ["FP","FU","U"], "old_struc":["VCV","VCV","VCV"]})
        uralonet_test.to_csv("uralonet_test.csv",encoding="utf-8",index=False)
        
        ad.launch(dfetymology="uralonet_test.csv",timelayer="",substituteclusters="substidict_test.txt",L2="whatever",substitutephons="whatever")
        
        self.assertDictEqual(ad.substidict,substidict_test)
        self.assertEqual(ad.wordstruc,["VCV"])
        self.assertEqual(ad.maxnrofclusters,3)
        
        substi_test=pd.DataFrame({"L2_phons": ["a","b","c","d"], "L1_substitutions": ["o","p","t","t"]})
        substi_test.to_csv("substi_test.csv",encoding="utf-8",index=False)
        dfgot_test=pd.DataFrame({"got_ipa":["aɸarsabbate","aɸaruh","aβrs"]})
        with open("dfgot_test.csv","w",encoding="utf-8") as data:
            data.write(str(dfgot_test))
        
        ad.launch(dfetymology="uralonet_test.csv",timelayer="",substituteclusters="",L2="dfgot_test.csv",substitutephons="substi_test.csv")
        self.assertCountEqual(ad.allowedclust,("ɑ","t͡ʃʲ","ðʲ","ɜ","l"))
        self.assertEqual(ad.maxclustlen,1)
        assert_frame_equal(ad.dfsubsti,substi_test)
        self.assertDictEqual(ad.sudict,{'a': 'o','b': 'p','c': 't','d':'t'})        
        
        os.remove("uralonet_test.csv")
        os.remove("substi_test.csv")
        os.remove("substidict_test.txt")        
        os.remove("dfgot_test.csv")
    
    def test_deletion(self):
        ad.maxclustlen=2
        ad.allowedclust={"e","i","j","jm","jr","jt͡ʃʲ","k","kl","ks","kt","l","lk","lm","m","mp","mt","n","nt","nʲ","nʲt͡ʃʲ","o","p","pp","r","s","t","tk","tt",\
                         "t͡ʃʲ","u","w","¨","æ","ð","ðʲ","ðʲk","ŋ","ŋs","ȣ","ɑ","ɜ","ɤ","ʃ","ʃʲ","ʃʲk"}
        ad.sudict={"a": "a, æ", "b": "p, m, w", "c": "t, s", "d": "t, n", "e": "e, i", "h": ", j, k, ŋ", "i": "i, e", "j": "j", "k": "k", "l": "l", "m": "m", \
                   "n": "n", "o": "o, u", "p": "p", "r": "r", "s": "s", "t": "t", "u": "u, o", "v": "w, p, u", "w": "w, u","x": "k, s", "y": "y", "z": "s, ʃʲ",\
                   "ð": "ð", "ŋ": "ŋ, k", "ɔ": "ɑ, o", "ɛ": "e, æ", "ɡ": "k, γ, ŋ", "ɣ": "ɣ", "ɪ": "i, e", "ɸ": "p, w, s", "β": "w, p, u", "θ": "t, s"}
        with patch("loanpy.adapter.ipa2tokens",side_effect=[["h", "t", "s"],["a","u","a","ɪ"]]):
            self.assertEqual(ad.deletion("hts"),"j, k, ŋ, t, s, kt, ks, ŋs")
            self.assertEqual(ad.deletion("auaɪ"),"æ, u, o, i, e")
            
    def test_clusters2substidict(self):
        ad.dfL2=pd.DataFrame({"ipa":["aɸarsabbate","aɸaruh","aβrs"]})
        ad.dfsubsti=pd.DataFrame({"L2_phons":["a","b","c","d","e","h","i","j","k","l","m","n","o","p","r","s","t","u","v","w","x","y","z","ð","ŋ","ɔ","ɛ","ɡ",\
                                                   "ɣ","ɪ","ɸ","β","θ"],\
                                  "L1_substitutions":["a, æ","p, m, w","t, s","t, n","e, i",", j, k, ŋ","i, e","j","k","l","m","n","o, u","p","r","s","t","u, o","w, p, u",\
                                                  "w, u","k, s","y","s, ʃʲ","ð","ŋ, k","ɑ, o","e, æ","k, γ, ŋ","ɣ","i, e","p, w, s","w, p, u","t, s"]})
        with patch("loanpy.adapter.flatten") as flatten_mock:
            flatten_mock.return_value=["a", "ɸ", "a", "rs", "a", "bb", "a", "t", "e","a", "ɸ", "a", "r", "u", "h","a", "βrs"]
            with patch("loanpy.adapter.deletion", side_effect=["p, m, w, pp, mp","r, s","w, p, u, r, s"]):
                ad.clusters2substidict(name="substidict_test")
                with open("substidict_test.txt", encoding="utf-8") as f:
                    sudict_test=f.read()
        self.assertEqual(sudict_test, str({"a": "a, æ", "b": "p, m, w", "c": "t, s", "d": "t, n", "e": "e, i", "h": ", j, k, ŋ", "i": "i, e", "j": "j", "k": "k","l": "l",\
                                           "m": "m", "n": "n", "o": "o, u", "p": "p", "r": "r", "s": "s", "t": "t", "u": "u, o", "v": "w, p, u", "w": "w, u", "x": "k, s",\
                                           "y": "y", "z": "s, ʃʲ", "ð": "ð","ŋ": "ŋ, k", "ɔ": "ɑ, o", "ɛ": "e, æ", "ɡ": "k, γ, ŋ", "ɣ": "ɣ", "ɪ": "i, e", "ɸ": "p, w, s", \
                                           "β": "w, p, u", "θ": "t, s", "bb": "p, m, w, pp, mp","rs": "r, s", "βrs": "w, p, u, r, s"}))
        os.remove("substidict_test.txt")
        
    def test_adapt1(self):
        self.assertEqual(ad.adapt1("bcdhxzɔɛɡɪɸβθl̥m̥n̥r̥aefi"),"pstkssɑækipwtVVVVaefi")
        
    def test_adapt2(self):
        with patch("loanpy.adapter.word2struc") as word2struck_mock:
            word2struck_mock.return_value="VCVC"
            ad.wordstruc=['VCVCV', 'CVCVCCV', 'CVCCV', 'CVCCCV', 'CV', 'CVCVCV','VCCCV', 'CVCVCC', 'CVCCVCV', 'VCCVCVCV', 'CVCV', 'VCCVCV', 'VCV', 'V', 'CVCCVCCV', 'VCCV']
            ed2op=[0.4,1.2000000000000002,1.8,2.2,2.0,0.8,1.8,0.8,1.2000000000000002,1.6,1.4,0.8,1.0,3.0,1.6,1.4]
            with patch("loanpy.adapter.editdistancewith2ops",side_effect=ed2op) as ed2op_mock:
                with patch("Levenshtein.editops") as edops:
                    edops.return_value=[('insert', 4, 4)]
                    with patch("Levenshtein.apply_edit") as apply_edit_mock:
                        apply_edit_mock.return_value="aβVsV"
                        with patch("loanpy.adapter.adapt1") as adapt1_mock:
                            adapt1_mock.return_value = "awVsV"
                            self.assertEqual(ad.adapt2("aβr̥s"),"awVsV")
                    
        #self.assertEqual(ad.adapt2("bcdhxzɔɛɡɪɸβθl̥m̥n̥r̥adef"),"pstkssɑækipwtVVVVadef")
        
    def test_adapt3(self):
        ad.maxnrofclusters=4
        ad.wordstruc={"CV", "CVCCV", "CVCV", "V", "VCCV", "VCV"}
        ad.substidict={"dr": "t, n, r","ɔ": "ɑ, o","hsn": "j, k, ŋ, s, n, ks, ŋs","a":"a, æ","m":"m","θl": "t, s, l","i": "i, e","s":"s"}
        word2struc_side_effect= ['CVCV','CVCV','CVCV','CVCV','CVCV','CVCV','CVCV','CVCV','CVCV','CVCV','CVCCV','CVCCV','CVCCV','CVCCV','CVCV','CVCV','CVCV',\
                                 'CVCV','CVCV','CVCV','CVCV','CVCV','CVCV','CVCV','CVCCV','CVCCV','CVCCV','CVCCV','CVCV','CVCV','CVCV','CVCV','CVCV','CVCV',\
                                 'CVCV','CVCV','CVCV','CVCV','CVCCV','CVCCV','CVCCV','CVCCV','CVCV','CVCV','CVCV','CVCV','CVCV','CVCV','CVCV','CVCV','CVCV',\
                                 'CVCV','CVCCV','CVCCV','CVCCV','CVCCV','CVCV','CVCV','CVCV','CVCV','CVCV','CVCV','CVCV','CVCV','CVCV','CVCV','CVCCV','CVCCV',\
                                 'CVCCV','CVCCV','CVCV','CVCV','CVCV','CVCV','CVCV','CVCV','CVCV','CVCV','CVCV','CVCV','CVCCV','CVCCV','CVCCV','CVCCV']
        word2struc_called_with= [call('tɑja'),call('tɑjæ'),call('tɑka'),call('tɑkæ'),call('tɑŋa'),call('tɑŋæ'),call('tɑsa'),call('tɑsæ'),call('tɑna'),\
                                 call('tɑnæ'),call('tɑksa'),call('tɑksæ'),call('tɑŋsa'),call('tɑŋsæ'),call('toja'),call('tojæ'),call('toka'),call('tokæ'),\
                                 call('toŋa'),call('toŋæ'),call('tosa'),call('tosæ'),call('tona'),call('tonæ'),call('toksa'),call('toksæ'),call('toŋsa'),\
                                 call('toŋsæ'),call('nɑja'),call('nɑjæ'),call('nɑka'),call('nɑkæ'),call('nɑŋa'),call('nɑŋæ'),call('nɑsa'),call('nɑsæ'),\
                                 call('nɑna'),call('nɑnæ'),call('nɑksa'),call('nɑksæ'),call('nɑŋsa'),call('nɑŋsæ'),call('noja'),call('nojæ'),call('noka'),\
                                 call('nokæ'),call('noŋa'),call('noŋæ'),call('nosa'),call('nosæ'),call('nona'),call('nonæ'),call('noksa'),call('noksæ'),\
                                 call('noŋsa'),call('noŋsæ'),call('rɑja'),call('rɑjæ'),call('rɑka'),call('rɑkæ'),call('rɑŋa'),call('rɑŋæ'),call('rɑsa'),\
                                 call('rɑsæ'),call('rɑna'),call('rɑnæ'),call('rɑksa'),call('rɑksæ'),call('rɑŋsa'),call('rɑŋsæ'),call('roja'),call('rojæ'),\
                                 call('roka'),call('rokæ'),call('roŋa'),call('roŋæ'),call('rosa'),call('rosæ'),call('rona'),call('ronæ'),call('roksa'),\
                                 call('roksæ'),call('roŋsa'),call('roŋsæ')]
        with patch("loanpy.adapter.ipa2clusters",side_effect=[["dr","ɔ","hsn","a"],["m","a","θl","i","s"]]) as ipa2clusters_mock:
            with patch("loanpy.adapter.word2struc", side_effect=word2struc_side_effect) as word2struc_mock:
                

                self.assertEqual(ad.adapt3("drɔhsna"), "tɑja, tɑjæ, tɑka, tɑkæ, tɑŋa, tɑŋæ, tɑsa, tɑsæ, tɑna, tɑnæ, tɑksa, tɑksæ, tɑŋsa, tɑŋsæ, toja, tojæ, toka, tokæ, toŋa, toŋæ, tosa, tosæ, tona, tonæ, toksa, "\
"toksæ, toŋsa, toŋsæ, nɑja, nɑjæ, nɑka, nɑkæ, nɑŋa, nɑŋæ, nɑsa, nɑsæ, nɑna, nɑnæ, nɑksa, nɑksæ, nɑŋsa, nɑŋsæ, noja, nojæ, noka, nokæ, noŋa, noŋæ, nosa, nosæ, nona, nonæ, "\
"noksa, noksæ, noŋsa, noŋsæ, rɑja, rɑjæ, rɑka, rɑkæ, rɑŋa, rɑŋæ, rɑsa, rɑsæ, rɑna, rɑnæ, rɑksa, rɑksæ, rɑŋsa, rɑŋsæ, roja, rojæ, roka, rokæ, roŋa, roŋæ, rosa, rosæ, rona, "\
"ronæ, roksa, roksæ, roŋsa, roŋsæ")
                
                self.assertEqual(ad.adapt3("maθlis"), "too long")
                self.assertEqual(ipa2clusters_mock.call_args_list, [call("drɔhsna"), call("maθlis")])
                self.assertEqual(word2struc_mock.call_args_list, (word2struc_called_with))
        del ad.maxnrofclusters
        del ad.wordstruc
        del ad.substidict
        
if __name__ == "__main__":
    unittest.main()