import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph=nx.Graph()
        self._idMapN={}

    def getAllRatings(self):
        return DAO.getAllRatings()

    def buildGraph(self, rat1, rat2):
        self._graph.clear()
        self._idMapN.clear()

        nodes=DAO.getAllNodes(rat1, rat2)
        for n in nodes:
            self._idMapN[n.id]=n

        self._graph.add_nodes_from(nodes)

        edges=DAO.getAllEdges(self._idMapN, rat1, rat2)
        for e in edges:
            self._graph.add_edge(e.n1, e.n2, weight=e.peso)


    def getGraphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)


    def get5BestEdges(self):
        archi=[]
        for u, v, peso in self._graph.edges(data=True):
            archi.append((u, v, peso["weight"]))
        archi.sort(key=lambda x: x[2], reverse=True)
        return archi[:5]

    def getConnectedComponents(self):
        compConn=nx.connected_components(self._graph)
        return list(compConn)

    def maxCompConnesse(self):
        compConn = nx.connected_components(self._graph)
        return max(compConn, key=len)



    def getBestPath(self):
        self._bestPath=[]
        parziale=[]
        for n in self._graph.nodes():
            parziale = [n]
            self._ricorsione(parziale)
        return self._bestPath

    def _ricorsione(self, parziale):
        #1) Condizione ottima
        if len(parziale)> len(self._bestPath):
            self._bestPath=copy.deepcopy(parziale)

        for n in self._graph.neighbors(parziale[-1]):
            if n in parziale:
                continue
            if n.date_of_birth > parziale[-1].date_of_birth:
                parziale.append(n)
                self._ricorsione(parziale)
                parziale.pop()



