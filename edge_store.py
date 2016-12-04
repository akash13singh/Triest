from collections import defaultdict
class edgestore:

    def __init__(self):
        self._store = {} # adjacency list
        self._num_edges = 0
        self._debug = True
        self._edge_set = set()


    def add(self,u,v):
        # print "adding edge (%s,%s)" % (u, v)
        # if (u,v) == ('2','3') or (u,v) == ('3','2'):
        #     print "hello"

        if u in self._store.keys():
            self._store[u].add(v)
        else :
            self._store[u]= set([v])

        if v in self._store.keys():
            self._store[v].add(u)
        else :
            self._store[v] = set([u])
        self._num_edges+=1
        self._edge_set.add((u,v))



    def delete(self,u,v):
        # if (u,v) == ('2','3') or (u,v) == ('3','2'):
        #     print "hello"
        #print "deleting edge (%s,%s)"%(u,v)
        self._store[u].remove(v)
        set_u = self._store[u]
        if len(set_u) == 0:
            del self._store[u]

        self._store[v].remove(u)
        set_v = self._store[v]
        if len(set_v) == 0:
            # print self._store
            # print "===========================================================deleting from defaultdict=========="
            del self._store[v]
            # print self._store

        self._num_edges -= 1
        self._edge_set.remove((u, v))



    def printContents(self):
        print self._store

    def get_neighbours(self,u):
        return self._store[u]


    def get_num_edges(self):
        return self._num_edges

    def get_num_vertices(self):
        return len(self._store)

    def get_vertice_list(self):
        return self._store.keys()

    def get_edges(self):
        return list(self._edge_set)

def testEdgeStore(datafile):
    edge_store = edgestore()
    f = open(datafile)
    for line in f:
        op,u,v = line.split()
        if op == '+':
            edge_store.add(u,v)
        elif op == "-":
            edge_store.delete(u,v)
    #print edge_store._store
    edge_store.printContents()
    print "neighbours of 3:"
    print edge_store.get_neighbours('3')
    edge_store.add(4,5)
    edge_store.printContents()
    edge_store.delete(4,5)
    edge_store.printContents()


if __name__ == '__main__':
    datafile = "data/dummy.txt"
    testEdgeStore(datafile)

