from __future__ import division
from edge_store import edgestore
from collections import defaultdict
import random
import matplotlib.pyplot as plt


class triest_impr:

    #triest setup
    def __init__(self,M):
        self._M = M
        self._S = edgestore()
        self._global_T = 0
        self._local_T = defaultdict(lambda:0)
        self._debug = True

    # Simulates flipping a coin
    # Params: head_prob : probability of Heads
    # Returns: if Heads return True else return False
    def flip_coin(self,head_prob):
        coin_toss = random.random()
        if coin_toss < head_prob :
            # print "Head"
            return True
        else:
            # print "Tail"
            return False


    #Updates local and global counters
    #Params:    t: timestamp,  (u,v): edge
    def update_counters(self,t,(u,v)):
        vertices = self._S.get_vertice_list()
        if u not in vertices or v not in vertices:
            return
        neighbourhood_u = self._S.get_neighbours(u)
        neighbourhood_v = self._S.get_neighbours(v)

        shared_neigbourhood = neighbourhood_u & neighbourhood_v
        shared_value = len(shared_neigbourhood)

        if shared_value == 0:
            return
        weight_t = ((t-1)*(t-2))/(self._M * (self._M-1) )
        if weight_t < 1:
            weight_t = 1
        for c in shared_neigbourhood:
                self._local_T[c]+= weight_t
                self._global_T += weight_t
                self._local_T[u] += weight_t
                self._local_T[v] += weight_t



    # impelemts reservoir sampling
    # Returns: if edge can be added to sample edgeset:S  else false
    def sample_edge(self,edge,t):
        # print "sample edge (%s,%s) at time %d)"%(edge[0],edge[1],t)
        if t <= self._M:
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
                return True

        return False

    #Run TRIEST-IMPR
    def run_triest_impr(self,datafile):
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
            if (u,v) in self._S.get_edges():
                #print "edge (%s,%s) already in sample"%(u,v)
                continue
            t=t+1
            self.update_counters(t,(u, v))
            if self.sample_edge((u,v),t):
                self._S.add(u,v)

        print "M = %d" % (self._M)
        print "Local Triangles %s"%(self._local_T)
        print "Global Triangles = %d" % (int(self._global_T))
        print "----------------------"
        return int(self._global_T)

def test_file(datafile):
    f = open(datafile)
    for line in f:
        u, v, weight = line.split()
        print "%s,%s"%(u,v)


if __name__ == '__main__':
    random.seed(14)
    #datafile = "data/dummy.txt"
    #datafile = "data/out.subelj_euroroad_euroroad"
    #datafile = "data/out.advogato"
    datafile = "data/out.petster-friendships-hamster-uniq"
    #M = [500,1000,1500,2000,2500,3000,3500,4000]
    M = [3000, 6000, 9000, 12000, 15000, 18000, 21000, 24000, 27000, 30000, 40000]
    triangles = []
    for m in M:
        obj = triest_impr(m)
        count = obj.run_triest_impr(datafile)
        triangles.append(count)
    plt.title("TRIEST-IMPR")
    plt.plot(M, triangles)
    plt.xlabel("M")
    plt.ylabel("Triangles")
    plt.xticks(M)
    plt.grid(True)
    plt.show()