# -*- coding: utf-8 -*-

import logging, re

from . import action


logger = logging.getLogger('xhamster')


_routeRe = re.compile(
    r'''^
        (?:https?:)?(?:\/\/)(?:www\.)?xhamster.com\/
        (?P<type>user\/(?:photo|video)|user|movies|photos\/gallery|photos\/view)\/
        (?P<identifier>[^\/]*)\/?
        (?P<extra>.*)
    $''',
    re.I | re.X
)

routes = {
    'movies': action.video,
    'photos/gallery': action.gallery,
    'photos/view': action.photo,
    'user': action.profile,
    'user/photo': action.userGalleryListing,
    'user/video': action.userVideoListing,
}

def routeByUrl(url):
    """Take a URL and .."""
    logger.info('Routing url={0}'.format(url))
    m = _routeRe.match(url)
    type_ = m.group('type')
    #print m.group('type'), m.group('identifier'), m.group('extra')
#    '''
#photos/view  1046191-17343648.html
#photos/gallery  1691678/huge_nipples_4.html
#user  Rbledsoe59
#movies  1430806/extreme_dildo_milf.html
#user/photo  Rbledsoe59/new-1.html
#user/video  Rbledsoe59/new-1.html
#    '''
    assert type_ in routes
    routes[type_](url, m.group('identifier'), m.group('extra'))

