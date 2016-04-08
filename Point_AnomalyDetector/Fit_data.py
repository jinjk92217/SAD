import numpy as np
import sys
from fitter import Fitter
import matplotlib.pyplot as plt
from cStringIO import StringIO
class Fit_data:
    def find_distribution(self,data,test_distribution=['norm']):
        para = self._fit_poisson(data = data)
        if float(para[1]) <= 0.1:
            return para
        para = self._fit_continuous(data=data,dist_list = test_distribution)
        return para
    def _fit_poisson(self,data):
        # if sum(i >=0.0 for i in data) <= 0.9 * len(data):
        #     return ['poisson',1.0,1.0]
        Max = int(max(data)) + 0.5
        entries, bin_edges, patches = plt.hist(data, bins=int(Max + 5.5), range=[-0.5, Max + 5], normed=True)
        plt.close()
        bin_middles = 0.5*(bin_edges[1:] + bin_edges[:-1])
        lamb = np.mean(data)
        total_error = 0.0
        for i in range(0,len(bin_middles)):
            total_error= total_error + np.abs(self._poisson_prob(int(bin_middles[i]),lamb) -entries[i] )
        return ['poisson',total_error,(lamb,)]

    def _fit_continuous(self,data,dist_list):
        #print "dist",data
        f = Fitter(data,distributions=dist_list)
        f.fit()
        # may take some time since by default, all distributions are tried
        # but you call manually provide a smaller set of distributions
        backup = sys.stdout
        sys.stdout = StringIO()
        f.summary()
        out = sys.stdout.getvalue()
        sys.stdout.close()  # close the stream
        sys.stdout = backup # restore original stdout

        distribution = out
        plt.close()
        #print distribution
        try:
            distribution = distribution.split("\n")[1].split(" ")
            distribution,error = distribution[0],distribution[-1]
        except Exception as e:
            return ['none',1.0]
        #print "ttttt",sys.stdout
        try:
            return [distribution,error,f.fitted_param[distribution]]
        except Exception as e:
            print "error",e
            return ['none',1.0]
    def _poisson_prob(self,k, lamb):
        p = np.exp(-lamb)
        for i in xrange(k):
            p *= lamb
            p /= i+1
        return p