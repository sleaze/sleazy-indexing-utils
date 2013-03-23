#!/usr/bin/env python

import os, sys, re
from cStringIO import StringIO


EXPANSION_REGION_RE = re.compile(r'''\[(?P<start>.*?)-(?P<stop>.*?)\]''', re.IGNORECASE)
NUMERIC_RE = re.compile(r'''^[0-9]+$''')

class PatternExpander(object):

    def __init__(self):
        pass

    def expand(self, string):
        m = EXPANSION_REGION_RE.search(string)
        if m:
            for intermediate in self._superExpand(string, m):
                yield intermediate
        else:
            yield string

    @staticmethod
    def _timeToStop(counters):
        for a, b in counters:
            if a <= b:
                return False
        return True

    def _superExpand(self, string, m):
        counters = []
        while m:
            try:
                counters.append([int(m.group('start')), int(m.group('stop'))])
            except ValueError:
                # It's not an integer.
                counters.append([m.group('start'), m.group('stop')])
            string = string.replace(m.group(0), '"', 1)
            m = EXPANSION_REGION_RE.search(string)
        while not self._timeToStop(counters):
            out = str(string)
            for i in range(0, len(counters)):
                out = out.replace('"', str(counters[i][0]), 1)
                if type(counters[i][0]) is int:
                    counters[i][0] += 1
                else:
                    # Increment non-numbers as ascii.
                    counters[i][0] = chr(ord(counters[i][0]) + 1)
            yield out


if __name__ == '__main__':

    filename = 'pe.txt'
 
    e = PatternExpander()

    with open(filename, 'r') as fh:
        for line in fh.read().split('\n'):
            line = line.strip()
            if len(line) > 0 and line[0] != ';' and line[0] != '#':
                for expanded in e.expand(line):
                    print expanded
    # assert( 

