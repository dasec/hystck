# Copyright (C) 2018 Sascha Kopp
# This file is part of hystck - http://hystck.fbi.h-da.de
# See the file 'docs/LICENSE' for copying permission.
# Utility function for pickling objects


import base64
try:
    import cPickle as pickle
except ImportError:
    import pickle as pickle


def base64pickle(obj):
    s = pickle.dumps(obj, 2)
    s = base64.b64encode(s)
    return s


def base64unpickle(string):
    s = base64.b64decode(string)
    o = pickle.loads(s)
    return o
