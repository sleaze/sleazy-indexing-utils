
import base64, re, urllib

try:
    from ..pyquery import PyQuery as pq
except ImportError:
    from pyquery import PyQuery as pq

from ..wget import *


SITES = [
    'http://plumpstars.com/',
]

linkExtractor = re.compile(r'.*out\.php.*url=[~]([^~]+)[~].*', re.I)

eventCounts = {}

def recordEvent(eventName):
    if eventName not in eventCounts:
        eventCounts[eventName] = 0
    eventCounts[eventName] += 1


def getCurrentGalleries():

    def extractRealLink(link):
        m = linkExtractor.match(link)
        if m:
            #print 'HEY! %s' % urllib2.unquote(base64.decodestring(m.group(1)))
            return urllib2.unquote(base64.decodestring(m.group(1)))
        else:
            # No decoding required.
            return link

    links = []
    for url in SITES:
        data = wget(url)
        d = pq(data)

        for a in d('.thumb a'):
            if 'href' in a.attrib:
                link = extractRealLink(a.attrib['href'])
                if link is not None:
                    links.append(link)
            else:
                recordEvent('linkHrefMissing')

    #print eventCounts
    #print links
    return links


