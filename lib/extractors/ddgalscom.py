
import re

try:
    from ..pyquery import PyQuery as pq
except ImportError:
    from pyquery import PyQuery as pq

from ..wget import *


SITES = [
    'http://www.elegantmatures.net/',
    'http://www.pornmaturepics.com/',
    'http://www.allmaturepics.net/',
    'http://www.hairymoms.net/',
    'http://www.uniquesexymoms.com/',
    'http://www.bushypussies.net/',
]

linkExtractor = re.compile(r'.*out\.cgi.*%u=([a-z0-9:\/\.]+)', re.I)

eventCounts = {}

def recordEvent(eventName):
    if eventName not in eventCounts:
        eventCounts[eventName] = 0
    eventCounts[eventName] += 1


def getCurrentGalleries():

    def extractRealLink(link):
        m = linkExtractor.match(link)
        if m:
            return m.group(1)
        else:
            recordEvent('linkExtractionFailures')
            return None

    links = []
    for url in SITES:
        data = wget(url)
        d = pq(data)

        for a in d('table.tabl a'):
            if 'href' in a.attrib:
                link = extractRealLink(a.attrib['href'])
                if link is not None:
                    links.append(link)
            else:
                recordEvent('linkHrefMissing')

    #print eventCounts
    #print links
    return links


