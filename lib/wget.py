#!/usr/bin/env python

import gzip, hashlib, os, urllib2

try:
    import cStringIO as StringIO
except:
    import StringIO

from OrderedDict import OrderedDict

from util import cache
from util.fs import *


DEBUG = False
#DEBUG = True

#USER_AGENT = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.10) Gecko/2009042316 Firefox/3.0.10)'
USER_AGENT = 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15'


class WgetError(Exception):
    pass

##_cache = OrderedDict()
##_cacheSizeLimit = 100
#CACHE_BASE_PATH = '.cache/wget'
#class Cache(object):
#    def set(self, key, data):
#        return filePutContents(self._constructPathFromKey(key), data)
#
#    def get(self, key):
#        return fileGetContents(self._constructPathFromKey(key))
#
#    def _constructPathFromKey(self, key):
#        k = hashlib.md5(key).hexdigest()
#        #print '%s/%s/%s/%s' % (CACHE_BASE_PATH, k[0], k[1], k)
#        return '%s/%s/%s/%s' % (CACHE_BASE_PATH, k[0], k[1], k)
#
#cache = Cache()


def wgetOpener(referer='http://www.google.com/GOBBLEGOBBLEGOBBLE'):
    opener = urllib2.build_opener()
    opener.addheaders = [
        ('User-Agent', USER_AGENT),
        ('Referer', referer),
    ]
    return opener

def wget(url, referer='', useCache=False, numTries=1, includeHeaders=False):
    """ 
    @param url URL to download.
    @param referer Defaults to ''.  If you pass None, it will be the same as
        the target URL.
    @param useCache whether or not a cached version is acceptable/desirable.
    @param numTries Number of retries in the event that an error occurs.
    @param includeHeaders When true, the return format will be in:
        `(data, responseHeaders)`.  When false, the return format will simply be
        `data`.
    """
    if includeHeaders:
        urlKey = 'headers+%s' % url
    else:
        urlKey = url

    if useCache: # and _cache.has_key(url) and len(_cache[url]):
        #return _cache[url]
        #if includeHeaders
        cached = cache.get(urlKey)
        if cached is not None:
            return cached

    if referer == '':
        referer = url
    opener = urllib2.build_opener()
    opener.addheaders = [
        ('User-Agent', USER_AGENT),
        ('Referer', referer),
        ('Accept-Encoding', 'gzip'),
    ]

    try:
        if DEBUG: print 'getting %s' % url

        response = opener.open(url)
        data = response.read()
        headers = response.info()
        # Make sure that anything containing uppercased keys has the equivalent
        # lower-cased version set.
        for k in headers:
            kLower = k.lower()
            if k != kLower:
                headers[kLower] = headers[k]

        # Attempt G-Zip extraction.  If it fails, no worries b/c there was
        # no compression.
        if 'content-encoding' in headers and 'gz' in headers['content-encoding'].lower():
            print 'ATTEMPTING DECOMPRESSION'
            try:
                compressedstream = StringIO.StringIO(data)
                gzipper = gzip.GzipFile(fileobj=compressedstream)
                data = gzipper.read()
            except IOError, e:
                print '[warn] wget - this was surprising, i couldn\'t decompress a response for url={%s} w/ cont-enc. value={%s}' % (url, headers['content-encoding'])
                print e
                pass

        if includeHeaders:
            out = (data, headers)
        else:
            out = data

        if useCache:
            #if len(_cache) > _cacheSizeLimit:
            #    del _cache[-1]
            #_cache[url] = data
            cache.set(url, out)

        return out

    except urllib2.URLError, e:
        if numTries > 1:
            return wget(url, referer, numTries - 1, includeHeaders)
        raise WgetError(url + ' failed, ' + str(e))

if __name__ == '__main__':
    url = 'http://fhg.stackedmamas.com/p202te/pics/images/moms25.jpg'
    ref = 'http://fhg.stackedmamas.com/p202te/pics/p2-1.php?nats=ODY2OjI6Nw,0'
    (data, headers) = wget(url=url, referer=ref, includeHeaders=True)
    print 'HEADERS: %s' % headers


