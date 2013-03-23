#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from lib.downloader import downloadGallery, downloadGalleries


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'missing required parameter: input filename'
        print 'usage: %s [input-filename]' % sys.argv[0]
        sys.exit(1)

    inputFile = sys.argv[1]

    downloadGalleries(inputFile)

            
