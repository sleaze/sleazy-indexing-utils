
from math import ceil

from OrderedDict import OrderedDict

"""
* This code was created by Jose Fonseca (josefonseca@blip.pt) 
*
* Please feel free to use it in either commercial or non-comercial applications,
* and if you enjoy using it feel free to let us know or to comment on our
* technical blog at http://code.blip.pt
"""


class KMeans(object):

    def __init__(self):
        self.is_keyed = False

    def distance(v1, v2):
        """
        * Calculates the distance (or similarity) between two values. The closer
        * the return value is to ZERO, the more similar the two values are.
        *
        * @param int v1
        * @param int v2
        *
        * @return int
        """
        return abs(v1-v2)

    def kmeans(self, data, k, dist_fun=None):
        """
        * This def takes a array of integers and the number of clusters to create.:
        * It returns a multidimensional array containing the original data organized
        * in clusters.
        *
        * @param array data
        * @param int k
        *
        * @return array
        """
        if dist_fun is None:
            dist_fun = self.distance

        if type(data) is dict:
        #if type(data) is tuple or type(data) is list:
            self.is_keyed = True
            self.orig_data = data
            data = data.values()
            #print data

        cpositions = self.assign_initial_positions(data, k, dist_fun)
        clusters = OrderedDict()
        while True:
            changes = self.kmeans_clustering(data, cpositions, clusters, dist_fun)
            if not changes:
                return self.kmeans_get_cluster_values(data, clusters, True)
            cpositions = self.kmeans_recalculate_cpositions(data, cpositions, clusters)

    def kmeans_clustering(self, data, cpositions, clusters, dist_fun):
        """
        """
        nChanges = 0
        for dataKey, value in enumerate(data):#.items():
            minDistance = None
            cluster = None
            #print cpositions
            for k, position in cpositions.items():
                #print 'position= ' , position
                dist = dist_fun(value, position)
                if None is minDistance or minDistance > dist:
                    minDistance = dist
                    cluster = k
            if not clusters.has_key(dataKey) or clusters[dataKey] != cluster:
                nChanges += 1
            clusters[dataKey] = cluster
        return nChanges

    def kmeans_recalculate_cpositions(self, data, cpositions, clusters):
        kValues = self.kmeans_get_cluster_values(data, clusters)
        for k, position in cpositions.items():
            if not kValues.has_key(k):
                cpositions[k] = 0
            else:
                cpositions[k] = self.kmeans_avg(kValues[k])
            #cpositions[k] = empty(kValues[k]) ? 0 : self.kmeans_avg(kValues[k])
        return cpositions

    def kmeans_get_cluster_values(self, data, clusters, final=False):
        values = {}#OrderedDict()

        if final and self.is_keyed:
            orig_keys = self.orig_data.keys()

        for i, (dataKey, cluster) in enumerate(clusters.items()):
            if not values.has_key(cluster):
                values[cluster] = []
            if final and self.is_keyed:
                values[cluster].append(orig_keys[dataKey])
            else:
                values[cluster].append(data[dataKey])
        return values

    def kmeans_avg(self, values):
        #return values[0]
        #print values
        n = len(values)
        total = sum(values)
        if n == 0:
            return 0
        else:
            return total / (n * 1.0)

    def assign_initial_positions(self, data, k, dist_fun):
        """
        * Creates the initial positions for the given
        * number of clusters and data.
        * @param array data
        * @param int k
        *
        * @return array
        """
        small = min(data)
        big = max(data)
        cpositions = OrderedDict()
        if k == 0:
            multiplier = 1
        else:
            multiplier = (dist_fun(small, big) * 1.0)/ k
        while k > 0:
            k -= 1
            try:
                cpositions[k] = small + multiplier * k 
            except TypeError:
                cpositions[k] = small
        #print cpositions
        return cpositions


    def sumascii(self, s):
        total = 0
        for char in s:
            total += ord(char)
        return total


def kmeans(data, k, dist_fun):
    return KMeans().kmeans(data, k, dist_fun)




if __name__ == '__main__':
    print kmeans([1, 3, 2, 5, 6, 2, 3, 1, 30, 36, 45, 3, 15, 17], 3)

    from levenshtein_distance import levenshtein_distance
    def f(a, b):
        print a,b
        return levenshtein_distance(a, b)
    print kmeans(['google', 'apple', 'mebo', 'bebo', 'bieber', 'connie', 'jay', 'ray', 'day', 'fay', 'paloalto', 'redwoodcity', 'cali', 'maui'], 3, f)

