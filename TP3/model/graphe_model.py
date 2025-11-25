import random
import threading

import networkx as nx
import matplotlib.pyplot as plt
from PyQt6.QtCore import pyqtSignal, QObject
from networkx import Graph


class GrapheModel(QObject):
    #Le graphe 0 à afficher
    _graphe:Graph = nx.Graph()
    #_pos contient le layout, soit le mapping noeud -> position pour l'Affichage
    _pos=None
    #contient le noeud selectionné
    _selected = None
    #numero à assigné aux noeuds
    _num_node : int = 10

    # probabilité qu'une arête existe entre deux nœuds pour la generation
    __proba=0.5
    # Le nombre de noeuds par défaut pour la generation
    __default_graphe_order =10
    # le poids min d'une arete pour la generation
    __poids_min = 1
    # le poids max d'une arete pour la generation
    __poids_max = 10

    # signal qui envoie le graphe complet
    grapheChanged = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self._pos = nx.spring_layout(self._graphe, seed=42)

    def graphe_order(self):
        return self._graphe.number_of_nodes()

    @property
    def default_graphe_order(self):
        return self.__default_graphe_order

    @default_graphe_order.setter
    def default_graphe_order(self, value):
        self.__default_graphe_order=value

    @property
    def graphe(self):
        return self._graphe

    @property
    def pos(self):
        return self._pos

    def edge_weight(self,edge):
        return  self._graphe[edge[0]][edge[1]]['weight']

    def generate_graph(self):
        # Générer un graphe aléatoire non orienté avec une probabilité d'Arete donnée
        self._graphe = nx.gnp_random_graph(self.default_graphe_order, self.__proba, directed=False)

        # Ajouter un poids aléatoire à chaque arête
        for u, v in self._graphe.edges():
            self._graphe[u][v]['weight'] = random.randint(self.__poids_min, self.__poids_max)

        # stocke le nouveau layout
        self._pos  = nx.spring_layout(self._graphe, seed=42)

        self._selected = None

        # Notif des vues
        self.grapheChanged.emit(self._pos )

    def delete_graph(self):
        # Effacer les references au graphe
        self._graphe = nx.empty_graph()
        # stocke le nouveau layout
        self._pos = nx.spring_layout(self._graphe, seed=42)

        # Notif des vues
        self.grapheChanged.emit(self._pos )

    #verifie si un noeud est présent à la position
    def verifierPos(self, position):
        positions = list(self._pos.values())
        hasPos = False
        for pos in positions:
            if pos[0] - 0.1 < position[0] < pos[0] + 0.1 and pos[1] - 0.1 < position[1] < pos[1] + 0.1:
                hasPos = True
        return hasPos

    def click_event(self, position):
        hasPos = self.verifierPos(position)
        if hasPos:
            self.select_node(position)
        else:
            self.add_node(position)

    def release_event(self, pos):
        hasPos = self.verifierPos(pos)

        if hasPos and self._selected[0] != pos[0] and self._selected[1] != pos[0]:
            pass


    def add_node(self, position):
        self._pos[self._num_node] = position
        self._graphe.add_node(self._num_node)
        self._num_node += 1

        self.grapheChanged.emit(self._pos)

    def select_node(self, position):
        for key, pos in self._pos.items():
            if pos[0] - 0.1 < position[0] < pos[0] + 0.1 and pos[1] - 0.1 < position[1] < pos[1] + 0.1:
                self._selected = key

        self.grapheChanged.emit(self._pos)

    def color_list(self):
        node_color = []
        for node in self._graphe.nodes():
            if node == self._selected:
                node_color.append('teal')
            else:
                node_color.append('skyblue')
        return node_color

    def delete_noeud(self):
        if self._selected is not None:
            del self._pos[self._selected]
            self._graphe.remove_node(self._selected)
            self._selected = None

            self.grapheChanged.emit(self._pos)