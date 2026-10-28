"""
Ejercicio 4: Metodo que retorne el camino exacto (lista de nodos) tras
ejecutar Dijkstra, no solo la distancia.
"""
import heapq
import math


class GrafoPonderado:

    def __init__(self, dirigido=False):
        self.adj = {}
        self.dirigido = dirigido

    def agregar_vertice(self, v):
        if v not in self.adj:
            self.adj[v] = []

    def agregar_arista(self, u, v, peso):
        self.agregar_vertice(u)
        self.agregar_vertice(v)
        self.adj[u].append((v, peso))
        if not self.dirigido:
            self.adj[v].append((u, peso))

    def dijkstra(self, inicio):
        distancias = {v: math.inf for v in self.adj}
        distancias[inicio] = 0
        pq = [(0, inicio)]
        while pq:
            dist_actual, actual = heapq.heappop(pq)
            if dist_actual > distancias[actual]:
                continue
            for vecino, peso in self.adj.get(actual, []):
                distancia = dist_actual + peso
                if distancia < distancias[vecino]:
                    distancias[vecino] = distancia
                    heapq.heappush(pq, (distancia, vecino))
        return distancias


    def dijkstra_con_previos(self, inicio):
        if inicio not in self.adj:
            raise KeyError(f"El vertice '{inicio}' no existe")
        distancias = {v: math.inf for v in self.adj}
        previos = {v: None for v in self.adj}
        distancias[inicio] = 0
        pq = [(0, inicio)]

        while pq:
            dist_actual, actual = heapq.heappop(pq)
            if dist_actual > distancias[actual]:
                continue
            for vecino, peso in self.adj[actual]:
                nueva = dist_actual + peso
                if nueva < distancias[vecino]:
                    distancias[vecino] = nueva
                    previos[vecino] = actual          # guardamos de dónde venimos
                    heapq.heappush(pq, (nueva, vecino))
        return distancias, previos

    def camino_minimo(self, inicio, destino):
        if destino not in self.adj:
            raise KeyError(f"El vertice '{destino}' no existe")
        distancias, previos = self.dijkstra_con_previos(inicio)

        if distancias[destino] == math.inf:
            return math.inf, []

        camino = []
        actual = destino
        while actual is not None:
            camino.append(actual)
            actual = previos[actual]
        camino.reverse()
        return distancias[destino], camino


if __name__ == "__main__":
    gp = GrafoPonderado()
    gp.agregar_arista('A', 'B', 4)
    gp.agregar_arista('A', 'C', 2)
    gp.agregar_arista('C', 'B', 1)
    gp.agregar_arista('B', 'D', 5)
    gp.agregar_vertice('Z')   # vertice aislado

    print("Distancias desde A:", gp.dijkstra('A'))
    dist, ruta = gp.camino_minimo('A', 'D')
    print(f"A -> D: {ruta}  distancia = {dist}")      # ['A','C','B','D'] = 8
    print("A -> A:", gp.camino_minimo('A', 'A'))       # (0, ['A'])
    print("A -> Z:", gp.camino_minimo('A', 'Z'))       # (inf, [])
