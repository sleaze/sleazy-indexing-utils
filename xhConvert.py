#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, glob
from pyquery import PyQuery as pq

i = 0
for filename in glob.glob('xhdata/*.html'): #os.walk('xhdata'):
    with open(filename, 'r') as fh:
        d = pq(fh.read())
        recent = d('div.imgListRecent a')
        images = map(lambda r: r.values()[0], filter(lambda r: len(r.values()) == 1, recent))
    with open(filename.replace('.html', '.txt'), 'w') as fh:
        fh.write('\n'.join(images))
    print i
    i += 1
