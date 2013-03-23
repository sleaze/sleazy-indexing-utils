#!/usr/bin/env python

from multiprocessing import Pool

from lib.extractors import elegantmaturesnet, plumpstarscom
from lib.downloader import downloadGallery

#from lib.LargestImage import extractMostCommonGroup
#from lib.util.fs import *
#from lib.wget import *
#
#
#def downloadGallery(galleryLink):
#    links = extractMostCommonGroup(galleryLink)
#    for link in links:
#        if not fileAlreadyDownloaded(link):
#            try:
#                data = wget(
#                    url=link,
#                    referer=galleryLink,
#                    useCache=True,
#                    numTries=3
#                )
#                saveDownloadedFile(link, data)
#            except Exception, e:
#                print 'ERROR: %s' % e
#	else:
#            print 'already downloaded %s' % link

def downloadAll():
    pool = Pool(1)#5)

    galleryLinks = plumpstarscom.getCurrentGalleries()
    pool.map(downloadGallery, galleryLinks)

    galleryLinks = elegantmaturesnet.getCurrentGalleries()
    pool.map(downloadGallery, galleryLinks)


if __name__ == '__main__':
    downloadAll()

