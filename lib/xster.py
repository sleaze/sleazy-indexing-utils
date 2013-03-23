#!/usr/bin/env python

import os, errno, re, sys, time

from pyquery import PyQuery as pq

from wget import *
from util.fs import *


galleryIdExtractor = re.compile(r'.*\/view\/([0-9]+)')

def xhamsterFindGalleryLink(url):
    try:
        if '/gallery/' in url:
            return url
        m = galleryIdExtractor.match(url)
        if m:
            print 'shortcut!'
            return 'http://xhamster.com/photos/gallery/%s/index.html' % m.group(1)
        try:
            data = wget(url=url, useCache=True)
            d = pq(data)
            link = d('.TitleTable a')[1]
            if '/gallery/' in link.attrib['href']:
                return link.attrib['href']
            else:
                raise Exception('No gallery found for url: %s' % url)
        except Exception, e:
            print 'exception: %s' % e
            return None
    except WgetError, e:
        raise

def xhamsterFindGalleryImages(url):
    try:
        try:
            data = wget(url, useCache=True, numTries=3)
        except Exception, e:
            print 'exception: %s' % e
            print 'falling back..'
            # Fallback to trying to find a gallery link.
            data = wget(url=xhamsterFindGalleryLink(url), useCache=True)
    
        d = pq(data)
        imagePageLinks = [imagePageLink for imagePageLink in d('table.img a') if '/photos/view/' in imagePageLink.attrib['href']]
        out = []
        for imagePageLink in imagePageLinks:
            out.append(imagePageLink.attrib['href'])
        return out
    except WgetError, e:
        raise

def xhamsterDownloadGallery(url):
    imagePageLinks = xhamsterFindGalleryImages(url)
    for imagePageLink in imagePageLinks:
        try:
            data = wget(url=imagePageLink, useCache=True, numTries=3)
        except WgetError, e:
            raise
        d = pq(data)
        imageElementCandidates = d('td#img img') # #imgSized')
        if len(imageElementCandidates) > 0:
            imageElement = imageElementCandidates[0]
            imageUrl = imageElement.attrib['src']
            if not fileAlreadyDownloaded(imageUrl):
                try:
                    imageData = wget(url=imageUrl, referer=imagePageLink, numTries=3)
                except WgetError, e:
                    raise
                saveDownloadedFile(imageUrl, imageData)
            else:
                print 'File already saved: %s' % imageUrl
        else:
            print 'No image found for imagePageLink=%s' % imagePageLink

def xhamsterDownloadGalleries(inputFile):
    """@param inputFile newline delimited links file, 1 per line."""
    with open(inputFile, 'r') as fh:
        urls = set([line.strip() for line in fh if len(line.strip()) > 0])
        for url in urls:
            try:
                galleryLink = xhamsterFindGalleryLink(url)
                print '[%s] downloading gallery: %s' % (time.localtime(), galleryLink)
                xhamsterDownloadGallery(galleryLink)
            except Exception, e:
                print '[ERROR] outermost loop caught exception: %s' % e


if __name__ == '__main__':
    if len(sys.argv) > 1:
        inputFile = sys.argv[1]
        if os.path.isfile(inputFile):
            xhamsterDownloadGalleries(inputFile)
        else:
            print 'error: invalid or non-existent file specified'
    else:
        print 'error: missing required parameter: input file'






