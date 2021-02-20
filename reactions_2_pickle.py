import pickle
from collections import Counter

def r2p(strings, fname):
    dict_counter_strings = dict(Counter(strings))
    pickle_out = open(fname,"wb")
    pickle.dump(dict_counter_strings, pickle_out)
    pickle_out.close()
