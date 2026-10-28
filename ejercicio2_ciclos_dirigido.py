"""
Ejercicio 2: Detectar si hay ciclos en un grafo dirigido.
"""

BLANCO, GRIS, NEGRO = 0, 1, 2

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

    # ------------------- LO QUE NOS PIDE EL EJERCICIO -------------------
    def tiene_ciclo(self):
        """Retorna True si el grafo dirigido contiene al menos un ciclo."""
        if not self.dirigido:
            raise ValueError("Este método es para grafos dirigidos")

        color = {v: BLANCO for v in self.adj}

        def visitar(u):
            color[u] = GRIS
            for v in self.vecinos(u):
                if color[v] == GRIS:          # arista de retroceso => ciclo
                    return True
                if color[v] == BLANCO and visitar(v):
                    return True
            color[u] = NEGRO
            return False

        # Se prueba desde cada vertice por si el grafo no es conexo
        for v in self.adj:
            if color[v] == BLANCO and visitar(v):
                return True
        return False


if __name__ == "__main__":
    # Sin ciclo (DAG): A->B->C, A->C
    g1 = Grafo(dirigido=True)
    g1.agregar_arista('A', 'B'); g1.agregar_arista('B', 'C'); g1.agregar_arista('A', 'C')
    print("DAG A->B->C, A->C        ->", g1.tiene_ciclo())      # False

    # Con ciclo: A->B->C->A
    g2 = Grafo(dirigido=True)
    g2.agregar_arista('A', 'B'); g2.agregar_arista('B', 'C'); g2.agregar_arista('C', 'A')
    print("A->B->C->A               ->", g2.tiene_ciclo())      # True

    # Bucle sobre si mismo
    g3 = Grafo(dirigido=True)
    g3.agregar_arista('X', 'X')
    print("X->X (bucle)             ->", g3.tiene_ciclo())      # True

    # Dos caminos que convergen (diamante) NO es ciclo
    g4 = Grafo(dirigido=True)
    for u, v in [('A', 'B'), ('A', 'C'), ('B', 'D'), ('C', 'D')]:
        g4.agregar_arista(u, v)
    print("Diamante A->B,C->D       ->", g4.tiene_ciclo())      # False

    # Ciclo en una componente separada
    g5 = Grafo(dirigido=True)
    g5.agregar_arista('A', 'B')
    g5.agregar_arista('M', 'N'); g5.agregar_arista('N', 'M')
    print("Ciclo en otra componente ->", g5.tiene_ciclo())      # True

    # Grafo vacio
    print("Grafo vacio              ->", Grafo(dirigido=True).tiene_ciclo())  # False
