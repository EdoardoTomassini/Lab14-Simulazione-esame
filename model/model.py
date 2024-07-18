import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):

        self._grafo = nx.DiGraph()
        self._nodes = []
        self._edges = []

        self._idMap = {}

        self._listChromosome = []
        self._listGenes = []
        self._listConnectedGenes = []

        self.loadGenes()
        self.loadChromosome()
        self.loadConnectedGenes()

    def buildGraph(self):
        self._grafo.clear()

        #riwìempio la lista si nodi preimpostata self._nodes
        for c in self._listChromosome:
            self._nodes.append(c)
        #aggiungo i nodi al grafo
        self._grafo.add_nodes_from(self._nodes)

        # per gli archi costruisco un dizionario anzichè una tuple
        # forse più utile perchè gli archi sono diretti
        edges = {}

        for g1, g2, corr in self._listConnectedGenes:
            if(self._idMap[g1], self._idMap[g2]) not in edges:
                edges[(self._idMap[g1], self._idMap[g2])] = float(corr)
            else:
                edges[(self._idMap[g1], self._idMap[g2])] += float(corr)

        #N.B, edges.items restituisce una tupla in cui il primo
        #elemento è la chiave e il secondo elemento è l valore del
        #dizionario -----> in questo caso la chiave è una tupla
        #a sua volta, per questo abbiamo usato questa scrittura
        # k[0] primo elemento della tupla e k[1] secondo elemento
        # della tupla
        for k, v in edges.items():
            self._edges.append((k[0], k[1], v))
        #aggiungo gli archi pesati al grafo:
        self._grafo.add_weighted_edges_from(self._edges)
        print(len(self._nodes))

    def getMaxWeightArchi(self):
        pass
    def getMinWeightArchi(self):
        pass



    def getGraphDetails(self):
        return len(self._nodes), len(self._edges)

    def loadGenes(self):
        self._listGenes = DAO.getAllGenes()
        for g in self._listGenes:
            self._idMap[g.GeneID] = g.Chromosome

    def loadChromosome(self):
        self._listChromosome = DAO.getAllChromosomes()

    def loadConnectedGenes(self):
        self._listConnectedGenes = DAO.getAllConnections()