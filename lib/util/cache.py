import hashlib, os, sys
from fs import mkdirs, dirname #, filePutContents, fileGetContents

try:
    import cPickle as pickle
except:
    import pickle

"""
@description A static singleton-esque file-based key/value cache.

@date 2012-04-19
"""

CACHE_BASE_PATH = '%s/.cache/wget' % dirname(sys.argv[0])

def set(key, data):
    #print 'storing %s => %s' % (key, data)
    filePath = _constructPathFromKey(key)
    parentPath = dirname(filePath)
    if not os.path.exists(parentPath):
        mkdirs(parentPath)
    with open(filePath, 'w') as fh:
        return pickle.dump(data, fh) #filePutContents(_constructPathFromKey(key), data)

def get(key):
    try:
        with open(_constructPathFromKey(key), 'r') as fh:
            return pickle.load(fh) #fileGetContents(_constructPathFromKey(key))
    except IOError:
        return None

def _constructPathFromKey(key):
    k = hashlib.md5(key).hexdigest()
    #print '%s/%s/%s/%s' % (CACHE_BASE_PATH, k[0], k[1], k)
    return '%s/%s/%s/%s' % (CACHE_BASE_PATH, k[0], k[1], k)

