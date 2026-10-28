"""
Ejercicio 5: Calcular el grado de entrada y de salida de cada nodo en un
grafo dirigido.
"""


class Grafo:
    def __init__(self, dirigido=False):
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

    
    def grados(self):
        
        if not self.dirigido:
            raise ValueError("Grado de entrada/salida aplica a grafos dirigidos")

        entrada = {v: 0 for v in self.adj}
        salida = {v: len(self.adj[v]) for v in self.adj}

        for u in self.adj:
            for v in self.adj[u]:
                entrada[v] += 1

        return {v: {'entrada': entrada[v], 'salida': salida[v]} for v in self.adj}

    def mostrar_grados(self):
        print(f"{'Nodo':10}{'Entrada':>9}{'Salida':>9}")
        for v, g in self.grados().items():
            print(f"{str(v):10}{g['entrada']:>9}{g['salida']:>9}")


if __name__ == "__main__":
    g = Grafo(dirigido=True)   # red social: A -> B significa "A sigue a B"
    g.agregar_arista('Alice', 'Bob')
    g.agregar_arista('Alice', 'Charlie')
    g.agregar_arista('Bob', 'Alice')
    g.agregar_arista('Charlie', 'Bob')
    g.agregar_arista('Diana', 'Alice')
    g.agregar_vertice('Eva')   # sin relaciones

    g.mostrar_grados()
    # Alice: entrada 2 (Bob, Diana), salida 2 | Bob: 2/1 | Charlie: 1/1 | Diana: 0/1 | Eva: 0/0

    r = g.grados()
    assert r['Alice'] == {'entrada': 2, 'salida': 2}
    assert r['Bob'] == {'entrada': 2, 'salida': 1}
    assert r['Eva'] == {'entrada': 0, 'salida': 0}
    # La suma de entradas debe ser igual a la suma de salidas (= nº de aristas)
    assert sum(x['entrada'] for x in r.values()) == sum(x['salida'] for x in r.values())
    print("\nVerificaciones correctas.")
