"""
Ejercicio 1: Escribir un metodo iterativo para DFS.
"""
class Grafo:
    def __init__(self, dirigido=False):
        """Grafo con lista de adyacencia (diccionario)."""
        self.adj = {}
        self.dirigido = dirigido

    def agregar_vertice(self, v):
        if v not in self.adj:
            self.adj[v] = []

    def agregar_arista(self, u, v):
        self.agregar_vertice(u)
        self.agregar_vertice(v)
        self.adj[u].append(v)
        if not self.dirigido:
            self.adj[v].append(u)

    def vecinos(self, v):
        return self.adj.get(v, [])

    def mostrar(self):
        for v, vecinos in self.adj.items():
            print(f"{v} -> {vecinos}")

    def dfs(self, inicio, visitados=None, resultado=None):
        """DFS recursivo (de la unidad), para comparar el orden."""
        if visitados is None:
            visitados = set()
            resultado = []
        visitados.add(inicio)
        resultado.append(inicio)
        for vecino in self.vecinos(inicio):
            if vecino not in visitados:
                self.dfs(vecino, visitados, resultado)
        return resultado

    # ------------------- LO QUE NOS PIDE EL EJERCICIO -------------------
    def dfs_iterativo(self, inicio):
        """Recorrido en profundidad usando una pila explicita."""
        if inicio not in self.adj:
            raise KeyError(f"El vertice '{inicio}' no existe en el grafo")

        visitados = set()
        pila = [inicio]
        resultado = []

        while pila:
            actual = pila.pop()              # sacamos el tope
            if actual in visitados:          # puede haberse apilado dos veces
                continue
            visitados.add(actual)
            resultado.append(actual)

            # Invertimos para conservar el orden natural de los vecinos
            for vecino in reversed(self.vecinos(actual)):
                if vecino not in visitados:
                    pila.append(vecino)

        return resultado


if __name__ == "__main__":
    g = Grafo()
    for u, v in [('A', 'B'), ('A', 'C'), ('B', 'D'), ('C', 'D'), ('D', 'E')]:
        g.agregar_arista(u, v)
    g.mostrar()

    print("DFS recursivo :", g.dfs('A'))
    print("DFS iterativo :", g.dfs_iterativo('A'))
    assert g.dfs('A') == g.dfs_iterativo('A')

    # Grafo con componentes desconectadas: solo se recorre la de 'inicio'
    g.agregar_arista('X', 'Y')
    print("Desde A (X-Y queda fuera):", g.dfs_iterativo('A'))
