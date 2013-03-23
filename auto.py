#!/usr/bin/env python

from lib.extractors import auto

from lib.wget import *


if __name__ == '__main__':
    url = 'http://www.dddgals.com/'
    url = 'http://www.amandapics.com'
    url = 'http://www.amandahome.com/?x=7960.5383.1518.'
    url = 'http://www.brigidasbigboobs.com/?x=9025.3858.'
    url = 'http://plumpstars.com/'
    url = 'http://www.mature51.com/'
    url = 'http://www.elegantmatures.net/'
    url = 'http://www.pornmaturepics.com/'
    url = 'http://www.allmaturepics.net/'
    url = 'http://www.hairymoms.net/'
    url = 'http://www.uniquesexymoms.com/'
    url = 'http://www.bushypussies.net/'
    url = 'http://www.jugride.com/'
    url = 'http://www.ladylana.com/?x=5767.5383.9025.'
    url = 'http://www.dianapost.com/'
    url = 'http://www.inlovewithboobs.com/'
    url = 'http://www.amandalist.com/'
    url = 'http://www.anyfoxy.com/'
    url = 'http://www.anysmut.com/?x=9839.8219.'
    url = 'http://www.mulligansmilfs.com/'
    url = 'http://www.mature-post.com/pictures/search/?q=Plump|Plumper&kwid=5677&c=1'
    url = 'http://www.coonyboobs.com/'
    url = 'http://www.bigtitsmilf.com/pics/mature-big-tits/'
    url = 'http://www.matureblast.com/main.php'
    url = 'http://www.momshere.com/'
    url = 'http://www.sexy-olders.com/'
    url = 'http://fresholders.com/'
    html = wget(url, referer=url)
    links = auto.autoExtractGalleryLinks(url, html)
    if links is not None:
        print links
        print 'url: %s, count: %s' % (url, len(links))
    else:
        print 'Failed, no matches found for url=%s' % url


