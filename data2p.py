#
import pickle
def data2p(data, fname):
    pickle_out = open(fname,"wb")
    pickle.dump(data, pickle_out)
    pickle_out.close()

