
import re

from LargestImage import extractMostCommonGroup
from util.fs import *
from wget import *
from PatternExpander import PatternExpander
from OrderedSet import OrderedSet

NUM_TRIES=3

def _downloadAndSaveFiles(links, referer=None):
    """Defaults to using each link as it's own referer."""
    r = referer
    for link in links:
        if referer is None:
            r = link
        if not fileAlreadyDownloaded(link):
            try:
                (data, headers) = wget(
                    url=link,
                    includeHeaders=True,
                    useCache=True,
                    referer=r,
                    numTries=NUM_TRIES
                )
                if 'content-type' in headers:
                    if 'image/' in headers['content-type'].lower():
                        saveDownloadedFile(link, data)
                    else:
                        pass
                else:
                    saveDownloadedFile(link, data)

            except WgetError, e:
                print '%s: (%s): %s' % (__file__, type(e), e)
            except Exception, e:
                print '%s: (%s): %s' % (__file__, type(e), e)
        else:
            print 'already downloaded %s' % link


# Cleaner upper regular expressions.
_urlQmarkStripperRe = re.compile(r'^([^?]+)(?:\?.*)*$')

def _cleanupHtmlLinkForStorage(link):
    """Cleans up the link in preparation of local storage."""
    m = _urlQmarkStripperRe.match(link)
    print m
    if m:
        link = m.group(1)
    if link[-1] == '/':
        link = '%s/index.html' % link
    if link[-5:].lower() != '.html':
        # Needs '.html' appended to it.
        link = '%s.html' % link
    print 'HI %s' % link
    return link

def downloadGallery(galleryLink):
    """
    Saves the passed image link or attempts to extract and download a group
    of links from the html."""
    try:
        (imageOrGalleryHtml, headers) = wget(
            url=galleryLink,
            includeHeaders=True,
            useCache=True,
            referer=galleryLink,
            numTries=NUM_TRIES
        )
        if 'content-type' in headers and 'image/' in headers['content-type'].lower():
            if not fileAlreadyDownloaded(galleryLink):
                saveDownloadedFile(galleryLink, imageOrGalleryHtml)
        else:
            links = extractMostCommonGroup(
                url=galleryLink,
                html=imageOrGalleryHtml
            )
            if links is not None:
                # Found a group to download.
                cleanedGalleryLink = _cleanupHtmlLinkForStorage(galleryLink)
                if not fileAlreadyDownloaded(cleanedGalleryLink):
                    saveDownloadedFile(cleanedGalleryLink, imageOrGalleryHtml)
                _downloadAndSaveFiles(links=links, referer=galleryLink)
            else:
                print '[warn] no link groups could be extracted from url=%s' % galleryLink
    except WgetError, e:
        print '%s: (%s): %s' % (__file__, type(e), e)


def downloadGalleries(fileName):
    e = PatternExpander()

    with open(fileName, 'r') as fh:
        lines = OrderedSet([line.strip() for line in fh])

    for line in lines:
        if len(line) > 0 and line[0] != '#' and line[0] != ';' and line[0] != '%':
            for result in e.expand(line):
                downloadGallery(line)

