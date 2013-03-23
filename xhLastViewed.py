#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re, time, pprint, os
from pyquery import PyQuery as pq

from lib.wget import *


_imageUrlParserRe = re.compile(r'^.*?\/view\/(?P<imageId>[0-9]+)-(?P<galleryId>[0-9]+)\.html.*$', re.I)

class Image(object):
    """XHamster image model."""

    def __init__(self, url):
        """Store reference to URL so the gallery or image id can be pulled if needed."""
        self.url = url
        self.seen = [time.time()] # Keep track of when and how many times the image has been "seen".

    # Cached results.
    _cachedParsedInfo = None

    def parsedInfo(self):
        """Get or build parser meta-data cache."""
        if self._cachedParsedInfo is None:
            self._cachedParsedInfo = _imageUrlParserRe.match(self.url)

        return self._cachedParsedInfo

    def imageId(self):
        """Infer the gallery and image ids from the URL."""
        return self.parsedInfo().group('imageId')
        
    def galleryId(self):
        """Infer the gallery and image ids from the URL."""
        return self.parsedInfo().group('galleryId')

    def __eq__(self, o):
        return hasattr(o, 'url') and o.url == self.url

    def __ne__(self, o):
        return not self.__eq__(o)

    def __repr__(self):
        return '["url": "{0}", "seenCount": "{1}", "seenLast": "{2}"]'.format(self.url, len(self.seen), max(self.seen))


def storeRecentImagesSnapshot(images):
    """Stores HTML data."""
    try:
        with open('xhdata/{0}.txt'.format(time.time()), 'w') as fh:
            fh.write('\n'.join(map(lambda i: i.url, images)))
    except Exception, e:
        print 'error: {0}'.format(e)


def storeImage(image, data):
    """Given an image with a url and the binary data, stores the image to the local disk."""
    imagePath = 'xhdata/images/{0}'.format(image.galleryId())
    if not os.path.exists(imagePath):
        os.makdedirs(imagePath)

    imagePath = '{0}/{1}.jpg'.format(imagePath, image.galleryId())
    if not os.path.exists(imagePath):
        with open(imagePath, 'wb') as fh:
            fh.write(data)


def getRecentlyViewed(startingUrl=None):
    """Retrieves and returns the list of recently viewed images."""
    if startingUrl is None:
        startingUrl = 'http://xhamster.com/photos/view/1612021-26469404.html#imgTop'

    data = wget(startingUrl)

    d = pq(data)
    
#    imageFileUrl = d('img#imgSized').attr.get('src', None)
#    if imageFileUrl is not None:
#        imageData = wget(imageFileUrl, referer=startingUrl)
#        storeImage(image.url, imageData)
#    #imgLink = d('img#imgSized')[0].values()

    recent = d('div.imgListRecent a')
    for r in recent:
        r.values()
    images = map(lambda r: Image(r.values()[0]), filter(lambda r: len(r.values()) == 1, recent))
    storeRecentImagesSnapshot(images)
    return images

def main():
    """d"""

    images = []

    startingUrl = None

    while 1:
        newImages = getRecentlyViewed(startingUrl)
        for i in newImages:
            if i not in images:
                images.append(i)
            else:
                # Add to seen.
                images[images.index(i)].seen.append(time.time())

        if len(newImages) > 0:
            startingUrl = newImages[-1].url
        # Sort by # of times seen, and then by most recently seen.
        images = sorted(images, key=lambda i: max(i.seen), reverse=True)
        images = sorted(images, key=lambda i: len(i.seen), reverse=True)
        pprint.pprint(images[0:30])

        time.sleep(3)




if __name__ == '__main__':
    main()

