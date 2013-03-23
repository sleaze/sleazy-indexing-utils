
import base64, re, urllib2

try:
    from ..pyquery import PyQuery as pq
except ImportError:
    from pyquery import PyQuery as pq


class TransformationDecorator(object):
    """Link sanity enforcement."""
    def __init__(self, fn):
        self.fn = fn

    def __call__(self, *args, **kw):
        return TransoformationDecorator.cleanupUrl(self.fn(*args, **kw))

    @staticmethod
    def cleanupUrl(u):
        if type(u) is str and '://' not in u[0:10]:
            u = 'http://%s' % u
        return u


"""
Generalized and [more] complex transformers.
"""

@TransformationDecorator
def basicExtractor(match):
    """Basic extractor"""
    return cleanupUrl(urllib2.unquote(match.group(1)))

@TransformationDecorator
def base64Extractor(match):
    """Base64 extractor"""
    return cleanupUrl(urllib2.unquote(base64.decodestring(match.group(1))))

@TransformationDecorator
def base64Rot13Extractor(match):
    """Base64 extractor"""
    decoded = base64.decodestring(('%s' % match.group(1)).encode('rot13'))
    return cleanupUrl(urllib2.unquote(decoded))

_ddgalsInnerExtractor = re.compile(r'.*url=(.*)', re.I)
@TransformationDecorator
def ddgalsTransformer(match):
    """ddgals extractor"""
    outer = base64Extractor(match)
    m2 = _ddgalsInnerExtractor.match(outer)
    if m2:
        return cleanupUrl(m2.group(1))
    else:
        return None


"""
Only valid matches will be passed to the `transform` lambda functions.
"""
extractors = [
    {
        'name'          : 'ddgals',
        'domQueries'    : ['table tr td a', 'div#content div.cat_thumb a', '.gallery a', '.thumbs a'],
        'example'       : 'st/st.php?id=3372&url=http://gallys.scoreland.com/images/TatianaBlair_25893/?nats=NTAwOTg0LjQuMi4yLjEuNzAyNDQyNi4wLjAuMA&p=',
        're'        : re.compile(r'^\/?st\/st\.php\?.*url=(https?:\/\/.*)$', re.I),
        'xFn'       : basicExtractor
    },
    {
        'name'          : 'amandapics',
        'domQueries'    : ['table tr td a'],
        'example'       : '/r/cT1pMHAyLjYwMzIzNTImdXJsPWh0dHA6Ly9nYWxsZXJpZXMyLmFkdWx0LWVtcGlyZS5jb20vNzgwOC8zNjgwMDUvMjY2Ni9pbmRleC5waHA=/***/',
        're'            : re.compile(r'^\/?r\/([a-z0-9_=+-]+)(\/\**\/)?$', re.I),
        'xFn'           : ddgalsTransformer
    },
    {
        'name'          : 'amandahome',
        'domQueries'    : ['table tr td a', '.pb a'],
        'example'       : '/v/cT1pNjhwMy4yOTcwNzUz/***/gals.kellymadison.com/tgp/1240874587.html%3Fnats%3Ddianapromo:paypersignup:kellymadison,0,0,0,251',
        're'            : re.compile(r'^\/?v\/.*\/\**\/(.*)$', re.I),
        'xFn'           : basicExtractor
    },
    {
        'name'          : 'plumpstars',
        'domQueries'    : ['div.thumb a', 'table tr td a'],
        'example'       : '/streamrotator/out.php?l=0.2.29.15693.210418&u=crtr/cgi/out.cgi?s=70&url=~aHR0cCUzQSUyRiUyRmdhbGx5cy5zY29yZWxhbmQuY29tJTJGZmx2cyUyRktyaXN0aU1heHhfMjc2ODklMkYlM0ZuYXRzJTNETVRBd01ERXlNekl1TkM0eUxqSXVNQzR3TGpBdU1DNHc=~',
        're'            : re.compile(r'^\/?(?:streamrotator|sr)\/out\.php\?.*(?:&|&amp;)?url=[~]([^~]+)[~].*', re.I),
        'xFn'           : base64Extractor
    },
    {
        'name'          : 'elegantmatures',
        'domQueries'    : ['table.tabl tr td a'],
        'example'       : 'dtr/link.php?gr=1&id=4b371f&url=/cgi-bin/te/o.cgi?s=60%u=http://www.hairymoms.net/matures/7e6558/',
        're'            : re.compile(r'\/?dtr/link.php\?.*%u=([a-z0-9:\/\.]+)', re.I),
        'xFn'           : basicExtractor
    },
    {
        'name'          : 'mature-post',
        'domQueries'    : ['.thumbs .itemContainerSub a'],
        'example'       : '/cgi-bin/atx/out.cgi?s=80&amp;c=1&amp;l=YTo3OntzOjE6ImMiO2k6MDtzOjM6InNpZCI7aToyMTE7czozOiJpaWQiO2k6ODtzOjM6ImdpZCI7czo2OiIzODEyMzgiO3M6NDoia3dpZCI7aTo1Njc3O3M6MzoicG9zIjtpOjE7czoyOiJycyI7aTo0O30=&amp;u=http://www.galleries.phatchecks.com/nfg/nfg37/?nats=MTA4MTozOjI',
        're'            : re.compile(r'\/?cgi-bin\/atx\/out\.cgi\?.*(?:&|&amp;)u=(.*)', re.I),
        'xFn'           : basicExtractor
    },
    {
        'name'          : 'matureblast',
        'domQueries'    : ['.content .thumb_big a', 'div.gals a'],
        'example'       : '/out.php?link=images/31x180x305&p=100&skip_sell=true&url=b64aHR0cDovL3JlYWxtYXR1cmVzd2luZ2Vycy5jb20vZ2FsbGVyaWVzL3d3dy9zbW9vdGhfcHVzc3lfc3ByZWFkc18vaW5kZXguc2h0bWw=',
        're'            : re.compile(r'\/?out\.php\?.*(?:&|&amp;)?url=(?:b64)?([^&]+)', re.I),
        'xFn'           : base64Extractor
    },
    {
        'name'          : 'bittitsmilf',
        'domQueries'    : ['.thumbs a'],
        'example'       : '',
        're'            : re.compile(r'\/?tr\/thumb\.php\?.*(?:&|&amp;)?u=(.*)', re.I),
        'xFn'           : basicExtractor
    },
]

_foundHttpUrlRe = re.compile(r'^(http|\/).*$', re.I)

def _applyExtractorFilter(x, d):
    """
    @param x Extractor which is a dict w/ name, domQuery, re and xFn indices.
    @param d PyQuery instance to query against.
    """
    matchingHrefs = []
    for q in x['domQueries']:
        for link in d(q):
            if 'href' in link.attrib:
                m = x['re'].match(link.attrib['href'])
                if m:
                    try:
                        found = x['xFn'](m)
                        if found is not None and _foundHttpUrlRe.match(found):
                            matchingHrefs.append(found)
                    except Exception, e:
                        print '%s: Got exception (%s): %s' % (__file__, type(e), e)
    if not len(matchingHrefs):
        return None
    else:
        return matchingHrefs

def autoExtractGalleryLinks(url, html):
    d = pq(html)
    for x in extractors:
        hrefs = _applyExtractorFilter(x, d)
        if hrefs is not None and len(hrefs):
            return hrefs
    return None

