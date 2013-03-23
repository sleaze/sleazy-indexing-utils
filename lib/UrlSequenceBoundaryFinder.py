#!/usr/bin/env python

from __future__ import division

import math, re, sys

from PatternExpander import PatternExpander

from wget import *


boundaries = [3, 57]



class ValidPageIdentifier(object):
    _invalidPageRe = re.compile(
       '(%s)' % '|'.join((
            'error: bad url or request',
            'bad or incorrect url',
            'requested url not found',
            'page not found',
            'bad request page'
        )),
        re.IGNORECASE | re.MULTILINE | re.DOTALL
    )

    def __init__(self, templateUrl):
        self.templateUrl = templateUrl

    def check(self, sub):
        try:
            data = wget(self.templateUrl % sub)
            if self._invalidPageRe.search(data) is not None:
                return False
        except Exception, e:
            print 'EXCEPTION: %s' % e
            return False
        return True


"""Holds info for easily doing binary expansion/reduction."""
class BoundsProperties(object):
    def __init__(self, templateUrl, start, numPad0s):
        self.templateUrl = templateUrl
        self.start = start
        self.reset()

    def reset(self, mode='-'):
        self.mode = mode
        self.index = self.start
        self.prevIndex = self.start

    def stepForward(self):
        delta = abs(self.index - self.prevIndex) * 2
        if delta == 0:
            delta = 1
        self.prevIndex = self.index
        if self.mode == '+':
            self.index += delta
        elif self.mode == '-':
            self.index -= delta
        return self.index

    def stepBackward(self):
        delta = int(math.ceil(abs(self.index - self.prevIndex) / 2))
        if delta == 0:
            delta = 1
        self.prevIndex = self.index
        if self.mode == '-':
            self.index += delta
        elif self.mode == '+':
            self.index -= delta
        return self.index


class UrlSequencyBoundaryFinder(object):

    _sequenceRe = re.compile(r'''.*\[([0-9]+)\].*''')
    _leadingZeroesRe = re.compile(r'''^(0+)''')

    @staticmethod
    def _numLeadingZeros(string):
        m = UrlSequencyBoundaryFinder._leadingZeroesRe.match(string)
        if m:
            return len(m.group(1))
        else:
            return 0

    def find(self, url):
        m = self._sequenceRe.match(url)
        if m:
            fragment = m.group(1)

            numPad0s = self._numLeadingZeros(fragment)
            start = int(m.group(1))
            templateUrl = re.sub(r'\[[0-9]+\]', '%s', url)

            bp = BoundsProperties(templateUrl, start, numPad0s)

            (lower, upper) = self._findLimits(bp)
            rnge = '[%s-%s]' % (lower, upper)
            return bp.templateUrl.replace('%s', rnge)
        else:
            return url

    def _findLimits(self, bp):
        validator = ValidPageIdentifier(bp.templateUrl)
        if not validator.check(bp.start):
            raise Exception("Invalid starting lower limit")
        else:
            lower = self._findLimit(bp, validator.check)
            bp.reset('+')
            upper = self._findLimit(bp, validator.check)
            return (lower, upper)

    def _findLimit(self, bp, checker):
        lastResult = True
        while True:
            result = checker(bp.index)
            # Debug:
            #print 'result=%s bp.index=%s lastResult=%s bp.prevIndex=%s' % \
            #    (result, bp.index, lastResult, bp.prevIndex)
            if abs(bp.prevIndex - bp.index) == 1:
                if lastResult and not result:
                    bp.index = bp.prevIndex
                    break
                if result and not lastResult:
                    break
            lastResult = result
            if result:
                bp.stepForward()
            else:
                bp.stepBackward()
        return bp.index

    """@param searchingDirection Char, '+' or '-'.
    def _checkInBounds(self, n, searchingDirection):
        if plusOrMinus == '-':
            if n >= boundaries[0]:
                return True
            else:
                return False
        elif plusOrMinus == '+':
            if n <= boundaries[1]:
                return True
            else:
                return False
        else:
            raise Exception('invalid plusOrMinus parameter to check function')"""





"""o = UrlSequencyBoundaryFinder.BoundsProperties("http://jay", 10, 0)
print o.stepForward()
print o.stepForward()
print o.stepForward()
print o.stepForward()
print o.stepForward()
print o.stepForward()
print o.stepBackward()
print o.stepForward()
print o.stepBackward()
print o.stepBackward()
print o.stepBackward()
print o.stepBackward()
print o.stepBackward()
print o.stepBackward()
print o.stepBackward()"""

args = sys.argv[1:]

bf = UrlSequencyBoundaryFinder()
for arg in args:
    print bf.find(arg)

