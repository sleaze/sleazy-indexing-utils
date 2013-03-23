#!/usr/bin/env python

import re, sys

from wget import *
from pyquery import PyQuery as pq

# from Pycluster.cluster import Record
#from Pycluster import kcluster
from kmeans import kmeans
from levenshtein_distance import levenshtein_distance
#from numpy import array

from pprint import pprint

import urlparse

import Image

try:
    import CStringIO as StringIO
except:
    import StringIO


containsNumberRe = re.compile(r'[^0-9][0-9]{0,9}[^0-9]')

def mean(values):
    l = len(values)
    if l == 0:
        return 0
    return sum(values) * 1.0 / l

def duplicates(lst):
    uniq = set(lst)
    dupes = [x for x in lst if lst.count(x) > 1]
    return set(dupes)

def excludeDuplicates(lst):
    dupes = duplicates(lst)
    non_dupes_only = [x for x in lst if x not in dupes]
    return non_dupes_only


completeUrlRe = re.compile(r'^(https?:)?\/\/', re.IGNORECASE)

#url_hostname_re = re.compile(r'^(https?:)?\/\/([^\/]+)(\/.*)?', re.IGNORECASE)

imageRe = re.compile(r'^.*\.(jpe?g|png|gif)$', re.IGNORECASE)

bodyOnlyRe = re.compile(r'^.*(<[ \t]*body[^>]*>.*<\/body[^>]*>).*$', re.M | re.I | re.S)

def extractMostCommonGroup(url, html=None):
## REQUIRING A HOSTNAME MATCH DOESN'T WORK FOR RELATIVE URLS..
#    match = url_hostname_re.match(url)
#    if match is not None:
#        hostname = match.group(2)
#    else:
#        raise Exception('Failed to extract hostname from the supplied url?')

#    a=array([[1,2,9,10,99,100], [3,4,10,11,99,150], [99, 100, 10, 13, 400, -3]])
#    mask=array([[1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1]])
#    clusterid, error, nfound = kcluster(a,
#        nclusters=2, mask=mask, weight=array([1, 1, 1, 1, 1, 1]),
#        transpose=0, npass=1000, method='a', dist='e')
#    print clusterid
#    print error
#    print nfound
#    return

    if html is None:
        html = wget(url)

    bodyOnlyMatch = bodyOnlyRe.match(html)
    if bodyOnlyMatch:
        d = pq(bodyOnlyMatch.group(1))
    else:
        print 'HTML: %s' % html
        print 'Warning: <body> tag region could not be extracted - this is bad'
        d = pq(html)

    def _print(x):
        print x
        return True

    #print [urlparse.urljoin(url, a.attrib['href']) for a in d('a')]
    lst = list(excludeDuplicates([
        urlparse.urljoin(url, a.attrib['href']) for a in d('a') if (
            #_print(pq(a).children('img')) and
            len(pq(a).children('img')) > 0 and
            a.attrib.has_key('href') and
            containsNumberRe.search(a.attrib['href'])
        )
    ]))

    #print lst


    domain = urlparse.urlsplit(url).netloc

    diffs = dict([
        (item, levenshtein_distance(lst[i].replace('http://', ''), domain))
        for i, item in enumerate(lst)
    ])

#     avg = mean(diffs)
#     print avg
#     print min(diffs)
#     print max(diffs)
#     pprint (lst)

    def f(a, b):
        return abs(a - b)

    numGroups = len(diffs) / 2
    print 'Num groups:',numGroups

    if len(diffs) == 0:
        print 'LargestImage extract.. error: no diffs!'
        return []

    groups = kmeans(diffs, numGroups, f)

    # Select and return the largest group of similar links.
    maxIdx = -1
    conflictedIdx = -1
    maxSz = 0
    for idx, group in groups.items():
        l = len(group)
        print l
        if l > maxSz:
            maxIdx = idx
            maxSz = l
            # Any previous conflict is no longer relevant.
            conflictedIdx = -1
        elif l == maxSz:
            # Mark conflicted state.
            conflictedIdx = idx

    print 'groups = %s' % groups
    # Make sure we got a result.
    if maxIdx == -1:
        raise Exception('No groups were found?  Very odd.. groups = %s' % groups)

    # Check to see if the largest group had conflicts.
    if conflictedIdx != -1:
        print 'WARNING: There was a group of equal size which was not selected.'

    imageLinks = False

    for link in groups[maxIdx]:
        if imageRe.match(link):
            imageLinks = True
            break

    if not imageLinks:
        print 'no image links were found.. for url=%s' % url
        out = []
        for link in groups[maxIdx]:
            out.append(extractLargestImageUrlFromUrl(link))
        return out

    #print 'imageLinks = %s' % imageLinks

    return groups[maxIdx]



def extractLargestImageUrlFromUrl(url, html=None, parentUrl=None):
    extractLargestImageFromUrl(url, html, parentUrl, True)

def extractLargestImageFromUrl(url, html=None, parentUrl=None, onlyUrl=False):
    """
    @param onlyUrl set to True to have only the url returned.
    """
    if parentUrl is None:
        parentUrl = url
    if html is None:
        html = wget(url=url, referer=parentUrl, useCache=True)

    print html
    d = pq(html)

    imageUrls = [
        urlparse.urljoin(url, img.attrib['src'])
        for img in d('img') if img.attrib.has_key('src')
    ]

    rawImages = []
    largestIdx = -1
    largestSz = 0
    conflictedIdx = -1
    for idx, image_url in enumerate(imageUrls):
        rawImageData = wget(
            url=imageUrls[idx],
            referer=parentUrl,
            useCache=True
        )
        rawImages.append(rawImageData)
        assert rawImages[idx] == rawImageData
        fakeFile = StringIO.StringIO(rawImages[-1])
        try:
            image = Image.open(fakeFile)
            print image.format, image.size
            sz = image.size[0] * image.size[1]
            print sz
            if sz > largestSz:
                largestIdx = idx
                largestSz = sz
                # Any previous conflict is no longer relevant.
                conflictedIdx = -1
            elif sz == largestSz:
                conflictedIdx = idx
        except IOError, e:
            print '%s: extractLargestImageUrlFromUrl Caught exception: (%s) %s' % (__file__, type(e), e)

    print largestIdx, conflictedIdx
    if conflictedIdx != -1:
        print 'WARNING: There was at least 1 additional image with equal dimensions'

    print 'largest image was #', largestIdx
    if largestIdx == -1:
        raise Exception('No images could be found at all!')
    if onlyUrl:
        return imageUrls[largestIdx]
    else:
        return rawImages[largestIdx]




if __name__ == '__main__':
    if len(sys.argv) > 1:
        #extractLargestImageUrlFromUrl(sys.argv[1])
        for arg in sys.argv[1:]:
            pprint(extractMostCommonGroup(arg))
    else:
        print 'please enter a url'
