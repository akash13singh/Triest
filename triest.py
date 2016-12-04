from __future__ import division
from edge_store import edgestore
from collections import defaultdict
import random


class triest:

    def __init__(self,M):
        self._M = M
        self._S = edgestore()
        self._global_T = 0
        self._local_T = defaultdict(lambda:0)
        self._debug = True

    # head_prob: probability of Heads.
    # if Heads return True else return False
    def flip_coin(self,head_prob):
        #print "head probability %f"%(head_prob)
        coin_toss = random.random()
        #print coin_toss
        if coin_toss < head_prob :
            # print "Head"
            return True
        else:
            # print "Tail"
            return False

    def update_counters(self,operation,(u,v)):
        vertices = self._S.get_vertice_list()
        if u not in vertices or v not in vertices:
            return
        neighbourhood_u = self._S.get_neighbours(u)
        neighbourhood_v = self._S.get_neighbours(v)

        shared_neigbourhood = neighbourhood_u & neighbourhood_v
        shared_value = len(shared_neigbourhood)

        if shared_value == 0:
            return

        if operation == '+':
            self._global_T +=  shared_value
            #print "global counter = %d. Incremented by %d"%(self._global_T,shared_value)
            self._local_T[u] +=  shared_value
            self._local_T[v] +=  shared_value

            for c in shared_neigbourhood:
                self._local_T[c]+= 1

        if operation == '-':
            self._global_T -= shared_value
            #print "global counter = %d. Decremented by %d" % (self._global_T, shared_value)

            self._local_T[u] -= shared_value
            if self._local_T[u] == 0:
                del self._local_T[u]

            self._local_T[v] -= shared_value
            if self._local_T[v] == 0:
                del self._local_T[v]

            for c in shared_neigbourhood:
                self._local_T[c]-= 1
            if self._local_T[c] == 0:
                del self._local_T[c]


    # impelemts reservoir sampling
    def sample_edge(self,edge,t):
        # print "sample edge (%s,%s) at time %d)"%(edge[0],edge[1],t)
        if t <= self._M:
            #print "space left for edge (%s,%s)"%(edge[0],edge[1])
            return True

        else:
            # print "No space for edge (%s,%s)" % (edge[0], edge[1])
            coin_toss = self.flip_coin(self._M/t)
            if coin_toss:
                edge_list = self._S.get_edges()
                num_edges = len(edge_list)
                e_idx = random.randint(0, num_edges-1)
                u1,v1 = edge_list[e_idx]
                # print "edge to be removed (%s,%s)" % (u1, v1)
                self._S.delete(u1, v1)
                #print "after deleting edge  "
                #print self._S.printContents()
                self.update_counters("-",(u1,v1))

                return True

        return False


    def run_triest(self,datafile):
        t = 0
        f = open(datafile)
        for line in f:
            input = line.split()
            u = input[0]
            v = input[1]
            if u==v :
                continue
            if u > v:
                tmp = u
                u = v
                v = tmp
            t=t+1
            # if t == 65:
            #     print "hello"
            #print "time %d"%(t)
            if self.sample_edge((u,v),t):
                self._S.add(u,v)
                #print "after adding the store is:"
                #print self._S.printContents()
                self.update_counters("+",(u,v))

        print "final Sample S: %s"%(self._S.printContents())

        print "golbal T %d"%(self._global_T)
        print "local T %s"%(self._local_T)
        print "sample edge set %s"%(self._S.get_edges())
        print "====Global Triangles %f======" % (self.estimate_triangles(t))


    def estimate_triangles(self,t):
        estimate = t*(t-1)*(t-2)/(self._M*(self._M-1)*(self._M-2))
        print "Estimate: %f"%(estimate)
        if estimate < 1:
            estimate =1
        return int(estimate) * self._global_T


def test_file(datafile):
    f = open(datafile)
    for line in f:
        u, v, weight = line.split()
        print "%s,%s"%(u,v)

if __name__ == '__main__':
    #random.seed(1234)
    #datafile = "data/dummy.txt"
    #datafile = "data/out.subelj_euroroad_euroroad"
    datafile = "data/out.advogato"
    obj = triest(40000)
    obj.run_triest(datafile)
    #test_file("data/out.moreno_bison_bison")