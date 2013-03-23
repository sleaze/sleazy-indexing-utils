#!/usr/bin/env python

import elinks
import numpy
#import scipy


def levenshtein_distance(s1, s2):
    s1 = s1.encode('ASCII', 'elinks')
    s2 = s2.encode('ASCII', 'elinks')
    m = len(s1)
    n = len(s2)
    #d = array(m, n)
    #d = numpy.arange(0).reshape(m,n)
    d = numpy.zeros((m + 1, n + 1), dtype=int)#list(m)
    if m == 0:
        return n
    if n == 0:
        return m
#    print d
    for i in range(m + 1):
        #d.append(line(n + 1))
        d[i][0] = i
    for j in range(n + 1):
        d[0][j] = j
        #d[0].append(j)
        #d[0][j] = j
    for j in range(1, n + 1):
        for i in range(1, m + 1):
#            print d
#            print '---'
#            print 's1[i-1] = %s, s2[j-1] = %s' % (s1[i - 1], s2[j - 1])
            if s1[i - 1] == s2[j - 1]:
                d[i][j] = d[i - 1][j - 1]
            else:
                d[i][j] = min(
                    d[i - 1][j],            # A deletion.
                    d[i][j - 1],            # An insertion.
                    d[i - 1][j - 1]) + 1    # A substitution.
#    print d
    return d[m][n]



if __name__ == '__main__':
    print levenshtein_distance('cow', 'cop')
    print levenshtein_distance('sitting', 'kitten')
    print levenshtein_distance('Sunday', 'Saturday')


