"""
Ejercicio 3: Grafo ponderado que represente una red de tráfico de red
y encontrar el camino de menor latencia
"""
import heapq
import math


class RedDeComputadoras:

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


    def latencia_minima(self, origen, destino):
        for nodo in (origen, destino):
            if nodo not in self.adj:
                raise KeyError(f"El dispositivo '{nodo}' no existe en la red")

        dist = self.dijkstra(origen)
        if dist[destino] == math.inf:
            return math.inf, []

        camino = [destino]
        actual = destino
        while actual != origen:
            for u in self.adj:                       # buscamos el predecesor
                for vecino, lat in self.adj[u]:
                    if vecino == actual and math.isclose(dist[u] + lat, dist[actual]):
                        actual = u
                        camino.append(u)
                        break
                else:
                    continue
                break
        camino.reverse()
        return dist[destino], camino


if __name__ == "__main__":
    red = RedDeComputadoras()  # enlaces bidireccionales
    enlaces = [
        ("PC-Oficina", "Switch-1", 1),
        ("Switch-1", "Router-A", 2),
        ("Switch-1", "Router-B", 5),
        ("Router-A", "Router-B", 2),
        ("Router-A", "Router-C", 10),
        ("Router-B", "Router-C", 3),
        ("Router-B", "Firewall", 4),
        ("Router-C", "Servidor-Web", 6),
        ("Firewall", "Servidor-Web", 2),
        ("Router-C", "Servidor-BD", 8),
    ]
    for a, b, ms in enlaces:
        red.agregar_arista(a, b, ms)
    red.agregar_vertice("Impresora-Aislada")   # dispositivo sin conexión

    print("Latencias minimas desde PC-Oficina:")
    for nodo, ms in red.dijkstra("PC-Oficina").items():
        print(f"  {nodo:18} {ms} ms")

    lat, ruta = red.latencia_minima("PC-Oficina", "Servidor-Web")
    print(f"\nMejor camino a Servidor-Web: {' -> '.join(ruta)}  ({lat} ms)")
    # Esperado: PC-Oficina -> Switch-1 -> Router-A -> Router-B -> Firewall -> Servidor-Web (11 ms)

    lat, ruta = red.latencia_minima("PC-Oficina", "Impresora-Aislada")
    print("A Impresora-Aislada:", "sin conexion" if not ruta else ruta)
