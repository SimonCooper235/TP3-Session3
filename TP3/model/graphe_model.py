import random
import threading

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from PyQt6.QtCore import pyqtSignal, QObject, QThread
from networkx import Graph

class GrapheModel(QObject):
    #Le graphe 0 à afficher
    _graphe:Graph = nx.Graph()
    #_pos contient le layout, soit le mapping noeud -> position pour l'Affichage
    _pos=None
    #contient le noeud sélectionné
    _selected = None
    #contient l'arête sélectionné
    _selected_edge = None
    #contient les chemin le plus court
    _chemin_court = None
    #numero à assigné aux noeuds
    _num_node = None

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

    def nombre_noeuds(self):
        return self._graphe.number_of_nodes()

    def generate_graph(self):
        # Générer un graphe aléatoire non orienté avec une probabilité d'Arete donnée
        self._graphe = nx.gnp_random_graph(self.default_graphe_order, self.__proba, directed=False)

        # Ajouter un poids aléatoire à chaque arête
        for u, v in self._graphe.edges():
            self._graphe[u][v]['weight'] = random.randint(self.__poids_min, self.__poids_max)

        # stocke le nouveau layout
        self._pos  = nx.spring_layout(self._graphe, seed=42)

        self._selected = None
        self._chemin_court = None
        self._num_node = 10

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

    def release_event(self, pos_init, pos_end, type):
        hasInit = self.verifierPos(pos_init)
        hasEnd = self.verifierPos(pos_end)
        same_pos = pos_init[0] == pos_end[0] and pos_init[1] == pos_end[1]

        if hasInit and hasEnd and type == "L" and same_pos:
            self.select_node(pos_init)
        elif hasInit and hasEnd and type == "R" :
            self.ajout_arete(pos_init, pos_end)
        elif hasInit and not hasEnd and type == "L" and not same_pos:
            self.move_node(pos_init, pos_end)
        elif not hasInit and not hasEnd and type == "L" and same_pos:
            self.trouv_arete(pos_end)


    def ajout_arete(self, pos_init, pos_end):
        noeud1 = None
        noeud2 = None
        nouv_arete = None
        for key, pos in self._pos.items():
            if pos[0] - 0.1 < pos_init[0] < pos[0] + 0.1 and pos[1] - 0.1 < pos_init[1] < pos[1] + 0.1:
                noeud1 = key
            if pos[0] - 0.1 < pos_end[0] < pos[0] + 0.1 and pos[1] - 0.1 < pos_end[1] < pos[1] + 0.1:
                noeud2 = key

        if noeud1 > noeud2 :
            nouv_arete = (noeud2, noeud1)
        else:
            nouv_arete = (noeud1, noeud2)

        if nouv_arete not in self._graphe.edges():
            self._graphe.add_edge(noeud1, noeud2, weight = 1)

        self.grapheChanged.emit(self._pos )


    def move_node(self, position1, position2):
        noeud1 = None
        for key, pos in self._pos.items():
            if pos[0] - 0.1 < position1[0] < pos[0] + 0.1 and pos[1] - 0.1 < position1[1] < pos[1] + 0.1:
                noeud1 = key

        self._pos[noeud1] = position2

        self.grapheChanged.emit(self._pos)

    def add_node(self, position):
        self._pos[self._num_node] = position
        self._graphe.add_node(self._num_node)
        self._num_node += 1

        self.grapheChanged.emit(self._pos)

    def select_node(self, position):
        for key, pos in self._pos.items():
            if pos[0] - 0.1 < position[0] < pos[0] + 0.1 and pos[1] - 0.1 < position[1] < pos[1] + 0.1:
                self._selected = key
                self._selected_edge = None

        self.grapheChanged.emit(self._pos)

    def color_list(self):
        node_color = []
        for node in self._graphe.nodes():
            if node == self._selected:
                node_color.append('teal')
            elif self._chemin_court != None and node in self._chemin_court:
                node_color.append('orange')
            else:
                node_color.append('skyblue')
        return node_color

    def delete(self):
        if self._selected is not None:
            del self._pos[self._selected]
            self._graphe.remove_node(self._selected)
            self._selected = None

        if self._selected_edge is not None:
            for edge in self.graphe.edges():
                if edge[0] == self._selected_edge[0] and edge[1] == self._selected_edge[1]:
                    self.graphe.remove_edge(edge[0], edge[1])

        self.grapheChanged.emit(self._pos)

    def trouver_chemin(self, debut, fin):
        self._chemin_court = nx.shortest_path(self._graphe, source=debut, target=fin, weight = 'weight')
        self.grapheChanged.emit(self._pos)

    def edge_color_list(self):
        edge_color = []
        edges = self._graphe.edges()
        sel = self._selected_edge
        colour_edge = None

        for edge in edges:
            if self._chemin_court is not None and len(self._chemin_court) > 1:
                if self._chemin_court[0] <= self._chemin_court[1]:
                    colour_edge = (self._chemin_court[0], self._chemin_court[1])
                else:
                    colour_edge = (self._chemin_court[1], self._chemin_court[0])

            if colour_edge is not None and edge[0] == colour_edge[0] and edge[1] == colour_edge[1]:
                self._chemin_court.remove(edge[0])
                edge_color.append('orange')
            elif sel is not None and edge[0] == sel[0] and edge[1] == sel[1] :
                edge_color.append('teal')
            else:
                edge_color.append('black')

        return edge_color

    def parcour_sommets(self, valeur):
        noeuds = self._pos.keys()
        list = []
        for noeud in noeuds:
            if noeud <= valeur:
                list.append(noeud)
        self._chemin_court = list

        self.grapheChanged.emit(self._pos)

    def distance_point_segment(self, clic, noeud1, noeud2):
        point_clic = np.array(clic)
        noeud1 = np.array(noeud1)
        noeud2 = np.array(noeud2)

        vect_noeuds = noeud2 - noeud1
        vect_clic_noeud1 = point_clic - noeud1

        vect_noeuds2 = np.dot(vect_noeuds, vect_noeuds)
        if vect_noeuds2 == 0:
            return np.linalg.norm(point_clic - noeud1)

        t = np.dot(vect_clic_noeud1, vect_noeuds) / vect_noeuds2
        t = max(0, min(1, t))
        closest = noeud1 + t * vect_noeuds
        return np.linalg.norm(point_clic - closest)

    def trouv_arete(self, clic, threshold = 0.02):
        closest_edge = None
        closest_distance = float('inf')

        for x, y in self._graphe.edges():
            noeud1 = self._pos[x]
            noeud2 = self._pos[y]

            dist = self.distance_point_segment(clic, noeud1, noeud2)

            if dist < closest_distance:
                closest_distance = dist
                closest_edge = (x, y)

        if closest_distance > threshold:
            self.add_node(clic)
        else:
            self._selected = None
            self._selected_edge = closest_edge
            self.grapheChanged.emit(self._pos)

    def modifier_poids(self, signe):
        arete = self._selected_edge

        if signe:
            self.graphe[arete[0]][arete[1]]['weight'] += 1
        else:
            self.graphe[arete[0]][arete[1]]['weight'] -= 1

        self.grapheChanged.emit(self._pos)

    def unsel(self):
        if self._selected is not None:
            self._selected = None
        elif self._selected_edge is not None:
            self._selected_edge = None

        self.grapheChanged.emit(self._pos)
