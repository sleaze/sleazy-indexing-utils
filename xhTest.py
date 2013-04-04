#!/usr/bin/env python
# -*- coding: utf-8 -*-

import fileinput, logging

from lib.xh import router
#from lib.xh.models import User #, Gallery, Video


logger = logging.getLogger('xhamster')


#session = Session()

#u = User(name="Rbledsoe59", createdTs='1434 days ago', modifiedTs='4 hours ago')

#session.add(u)
#session.commit()


#router.routeByUrl('http://xhamster.com/photos/view/1046191-17343648.html')
#router.routeByUrl('http://xhamster.com/photos/gallery/1691678/huge_nipples_4.html')
#router.routeByUrl('http://xhamster.com/user/Rbledsoe59')
#router.routeByUrl('http://xhamster.com/movies/1772212/chubby_girl_playtime.html')
#router.routeByUrl('http://xhamster.com/movies/1430806/extreme_dildo_milf.html')
#router.routeByUrl('http://xhamster.com/user/photo/Rbledsoe59/new-1.html')
#router.routeByUrl('http://xhamster.com/user/video/Rbledsoe59/new-1.html')


import multiprocessing, subprocess

from lib import settings

def doIt(url):
    try:
        router.routeByUrl(url)
    except:
        try:
            router.routeByUrl(url)
        except Exception, e:
            print 'CAUGHT E on 2nd attempt: %s' % (e,)

#lines = filter(
#with open(settings.basePath + '/urls.txt', 'r') as fh:
#    lines = filter(lambda line: len(line.strip()) != 0, fh.readlines())

pool = multiprocessing.Pool(25)
r = pool.map(doIt, filter(lambda line: len(line.strip()) != 0, fileinput.input()), chunksize=10)
#r = pool.map(router.routeByUrl, fh.readlines(), chunksize=10)
pool.close()
#r.wait()
#pool.join()

