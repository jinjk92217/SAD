"""
:copyright: (c) 2016 Tomas Olsson
:license: LGPL?
"""
from sklearn.neighbors.base import KNeighborsMixin

__author__ = 'tol'

class LOF:
    def __init__(self, knn):
        '''
        Class LOF implements the Local Outlier Factor algorithm,
        see http://www.dbs.ifi.lmu.de/Publikationen/Papers/LOF.pdf.
        It uses the scikit-learn nearest neighbour algorithm to retrieve neighbours and
        compute anomaly scores for data given a training set in the knn. So, for updating
        the algorithm, the knn instance should be updated.

        :param knn: an instance of klearn.neighbors.base.KNeighborsMixin, for instance, sklearn.neighbors.unsupervised.NearestNeighbors
        :return:
        '''
        assert isinstance(knn, KNeighborsMixin)
        self._knn = knn

        self._kdistance = {}
        self._lrd = {}
        self._Nk = {}


    def anomaly_score(self, X, in_training_set=False):
        '''
        :param X: an array containing data to score
        :param in_training_set: a boolean that indicates whether the scored data set is present in the training data set.
        :return: an anomly score for each data point in X
        '''
        lrd_a = 0
        lof_score = [0 for _ in range(len(X))]
        for a in range(len(X)):
            if in_training_set:
                self._check_and_add_kdistance_and_lrd_b(a)
                kdistance_a = self._kdistance[a]
                lrd_a = self._lrd[a]
                Nka = self._Nk[a]
                for b in Nka:
                    self._check_and_add_kdistance_and_lrd_b(b)
            else:
                d,nn = self._knn.kneighbors(X, min([self._knn.n_neighbors+100, len(self._knn._fit_X)-1]))
                kdistance_a = d[a][self._knn.n_neighbors-1]

                Nka = nn[a][d[a] <= kdistance_a]

                d2b = {}
                for b in Nka:
                    self._check_and_add_kdistance_and_lrd_b(b)
                    d2b[b] = d[a][nn[a]==b][0]
                    #print "d2b", d2b[b]

                lrd_a = self._compute_lrd(self._kdistance, d2b, Nka)

            lof_score[a] = (sum([self._lrd[b] for b in Nka])/len(Nka))/lrd_a

            #print "lrd_a", lrd_a, len(Nka), kdistance_a, [self._lrd[b] for b in Nka], sum([self._lrd[b] for b in Nka])

        return lof_score

    def anomaly_score_training_data(self):
        return self.anomaly_score(self._knn._fit_X, in_training_set=True)

    def _compute_lrd(self, kdistance_b, dist_a_b, Nka):
        return len(Nka)/sum([max([kdistance_b[b], dist_a_b[b]]) for b in Nka])

    def _check_and_add_kdistance_and_lrd_b(self, b):
        if not self._kdistance.has_key(b) or not self._lrd.has_key(b):
            d0, nn0 = self._knn.kneighbors([self._knn._fit_X[b]], min([self._knn.n_neighbors + 100, len(self._knn._fit_X)-2]))

            if not self._kdistance.has_key(b):
                self._kdistance[b] = d0[0][self._knn.n_neighbors]

            if not self._lrd.has_key(b):
                Nkb = nn0[0][d0[0] <= self._kdistance[b]]
                self._Nk[b] = Nkb[Nkb != b]

                d2c = {}
                for c in self._Nk[b]:
                    d2c[c] = d0[0][nn0[0] == c][0]
                    if not self._kdistance.has_key(c):
                        d00, n00 = self._knn.kneighbors([self._knn._fit_X[c]], self._knn.n_neighbors + 1)
                        self._kdistance[c] = d00[0][self._knn.n_neighbors]

                self._lrd[b] = self._compute_lrd(self._kdistance, d2c, self._Nk[b])
