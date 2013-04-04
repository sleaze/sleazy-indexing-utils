#!/usr/bin/env python
# -*- coding: utf-8 -*-

import itertools, fileinput, logging, sys, multiprocessing, subprocess

from lib import settings
from lib.xh import router


logger = logging.getLogger('xhamster')

PARALLEL = True


#router.routeByUrl('http://xhamster.com/photos/view/1046191-17343648.html')
#router.routeByUrl('http://xhamster.com/photos/gallery/1691678/huge_nipples_4.html')
#router.routeByUrl('http://xhamster.com/user/Rbledsoe59')
#router.routeByUrl('http://xhamster.com/movies/1772212/chubby_girl_playtime.html')
#router.routeByUrl('http://xhamster.com/movies/1430806/extreme_dildo_milf.html')
#router.routeByUrl('http://xhamster.com/user/photo/Rbledsoe59/new-1.html')
#router.routeByUrl('http://xhamster.com/user/video/Rbledsoe59/new-1.html')

def doIt(url):
    if len(url.strip()) == 0:
        return
    try:
        return router.routeByUrl(url)
    except:
        try:
            return router.routeByUrl(url)
        except Exception, e:
            print 'CAUGHT E on 2nd attempt: %s' % (e,)

if PARALLEL is True:
    logger.info('Operating in parallel')
    pool = multiprocessing.Pool(25)
    #r = pool.imap_unordered(doIt, itertools.ifilter(lambda line: len(line.strip()) != 0, fileinput.input()), chunksize=10)
    [x for x in pool.imap_unordered(doIt, fileinput.input(), chunksize=10)]
    #r = pool.map(doIt, filter(lambda line: len(line.strip()) != 0, fileinput.input()), chunksize=10)
    #print itertools.ifilter(lambda line: len(line.strip()) != 0, fileinput.input())
    #r = pool.map(doIt, itertools.ifilter(lambda line: len(line.strip()) != 0, sys.stdin.readlines()), chunksize=10)
    try:
        pool.close()
        pool.join()
    except TypeError:
        pass

    #r = pool.map(router.routeByUrl, fh.readlines(), chunksize=10)
    #r.wait()
    #pool.join()
else:
    logger.info('Operating serially')
    map(doIt, filter(lambda line: len(line.strip()) != 0, fileinput.input()))


