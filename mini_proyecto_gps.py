"""
Mini-Proyecto: Sistema de Navegación GPS (Unidad 10 - Grafos)
"""
import heapq
import math


# ----------------------------------------------------------------------
# Excepciones propias (manejo de errores claro y especifico)
# ----------------------------------------------------------------------
class ErrorGPS(Exception):
    """Clase base de los errores del sistema."""


class CiudadNoExisteError(ErrorGPS):
    pass


class TiempoInvalidoError(ErrorGPS):
    pass


class RutaInvalidaError(ErrorGPS):
    pass


class SinRutaError(ErrorGPS):
    pass


# ----------------------------------------------------------------------
# Grafo ponderado (lista de adyacencia)
# ----------------------------------------------------------------------
class GrafoPonderado:
    """Grafo no dirigido y ponderado.  adj = {ciudad: {vecino: minutos}}"""

    def __init__(self):
        self.adj = {}

    # --- Ciudades -------
    def agregar_ciudad(self, nombre):
        if not nombre or not nombre.strip():
            raise ValueError("El nombre de la ciudad no puede estar vacio")
        self.adj.setdefault(nombre, {})

    def buscar_ciudad(self, texto):
        """Búsqueda sin distinguir mayusculas/espacios. Retorna el nombre real."""
        clave = texto.strip().lower()
        for ciudad in self.adj:
            if ciudad.lower() == clave:
                return ciudad
        raise CiudadNoExisteError(f"La ciudad '{texto.strip()}' no esta registrada")

    def ciudades(self):
        return sorted(self.adj)

    # --- Autopistas ------
    def agregar_autopista(self, a, b, minutos):
        if a.strip().lower() == b.strip().lower():
            raise RutaInvalidaError("Una autopista debe unir dos ciudades distintas")
        if isinstance(minutos, bool) or not isinstance(minutos, (int, float)):
            raise TiempoInvalidoError("El tiempo debe ser un numero")
        if math.isnan(minutos) or math.isinf(minutos) or minutos <= 0:
            raise TiempoInvalidoError("El tiempo debe ser mayor que 0 minutos")

        existia = b in self.adj.get(a, {})
        self.agregar_ciudad(a)
        self.agregar_ciudad(b)
        self.adj[a][b] = minutos
        self.adj[b][a] = minutos
        return existia

    def autopistas(self):
        """Lista (a, b, minutos) sin duplicar la direccion inversa."""
        vistas, lista = set(), []
        for a in sorted(self.adj):
            for b, t in sorted(self.adj[a].items()):
                if (b, a) not in vistas:
                    vistas.add((a, b))
                    lista.append((a, b, t))
        return lista

    # --- Dijkstra con reconstruccion de ruta -------
    def ruta_mas_rapida(self, origen, destino):
        """
        Retorna (minutos_totales, [ciudades del recorrido]).
        Lanza CiudadNoExisteError o SinRutaError segun el caso.
        """
        origen = self.buscar_ciudad(origen)
        destino = self.buscar_ciudad(destino)

        distancias = {c: math.inf for c in self.adj}
        previos = {c: None for c in self.adj}
        distancias[origen] = 0
        pq = [(0, origen)]

        while pq:
            dist_actual, actual = heapq.heappop(pq)
            if dist_actual > distancias[actual]:
                continue                      # entrada desactualizada
            if actual == destino:
                break                         # ya es el minimo, no seguimos
            for vecino, minutos in self.adj[actual].items():
                nueva = dist_actual + minutos
                if nueva < distancias[vecino]:
                    distancias[vecino] = nueva
                    previos[vecino] = actual
                    heapq.heappush(pq, (nueva, vecino))

        if distancias[destino] == math.inf:
            raise SinRutaError(f"No existe ninguna ruta entre {origen} y {destino}")

        recorrido = []
        actual = destino
        while actual is not None:             # reconstruccion hacia atras
            recorrido.append(actual)
            actual = previos[actual]
        recorrido.reverse()
        return distancias[destino], recorrido


# ----------------------------------------------------------------------
# Utilidades de presentacion y entrada
# ----------------------------------------------------------------------
def formatear_tiempo(minutos):
    minutos = round(minutos)
    h, m = divmod(minutos, 60)
    if h and m:
        return f"{h} h {m} min"
    if h:
        return f"{h} h"
    return f"{m} min"


def leer_texto(mensaje):
    while True:
        valor = input(mensaje).strip()
        if valor:
            return valor
        print("  ! Este dato es obligatorio.")


def leer_minutos(mensaje):
    while True:
        texto = input(mensaje).strip().replace(",", ".")
        try:
            valor = float(texto)
        except ValueError:
            print("  ! Escribe un numero valido (ej. 45).")
            continue
        if math.isnan(valor) or math.isinf(valor) or valor <= 0:
            print("  ! El tiempo debe ser mayor que 0.")
            continue
        return int(valor) if valor.is_integer() else valor



def cargar_datos_iniciales(g):
    """Mapa de ejemplo (tiempos aproximados en minutos)."""
    datos = [
        ("Managua", "Masaya", 25), ("Managua", "Granada", 50),
        ("Masaya", "Granada", 25), ("Managua", "Jinotepe", 55),
        ("Jinotepe", "Rivas", 60), ("Granada", "Rivas", 80),
        ("Managua", "León", 75), ("León", "Chinandega", 60),
        ("Managua", "Matagalpa", 120), ("Matagalpa", "Estelí", 75),
        ("Managua", "Estelí", 150), ("Managua", "Juigalpa", 110),
        ("Juigalpa", "Matagalpa", 130),
    ]
    for a, b, t in datos:
        g.agregar_autopista(a, b, t)
    g.agregar_ciudad("Bluefields")   # ciudad sin autopistas conectadas (caso limite)


# ----------------------------------------------------------------------
# Opciones del menu
# ----------------------------------------------------------------------
def opcion_ver_ciudades(g):
    ciudades = g.ciudades()
    if not ciudades:
        print("\nNo hay ciudades registradas.")
        return
    print(f"\nCiudades registradas ({len(ciudades)}):")
    for i, c in enumerate(ciudades, 1):
        vecinos = g.adj[c]
        detalle = ", ".join(f"{v} ({t} min)" for v, t in sorted(vecinos.items()))
        print(f"  {i:>2}. {c:<12} -> {detalle if detalle else 'sin autopistas'}")


def opcion_agregar_ruta(g):
    print("\n--- Agregar nueva ruta ---")
    a = leer_texto("Ciudad A: ")
    b = leer_texto("Ciudad B: ")
    # Si la ciudad ya existe (aunque se escriba distinto), se usa su nombre real
    try:
        a = g.buscar_ciudad(a)
    except CiudadNoExisteError:
        a = a.strip().title()
    try:
        b = g.buscar_ciudad(b)
    except CiudadNoExisteError:
        b = b.strip().title()
    if a.lower() == b.lower():
        raise RutaInvalidaError("Una autopista debe unir dos ciudades distintas")
    minutos = leer_minutos("Tiempo en minutos: ")
    existia = g.agregar_autopista(a, b, minutos)
    accion = "actualizada" if existia else "agregada"
    print(f"\nAutopista {accion}: {a} <-> {b} ({minutos} min)")


def opcion_consultar_ruta(g):
    print("\n--- Ruta mas rapida ---")
    if len(g.adj) < 2:
        raise SinRutaError("Se necesitan al menos dos ciudades registradas")
    origen = leer_texto("Ciudad de origen: ")
    destino = leer_texto("Ciudad de destino: ")
    minutos, recorrido = g.ruta_mas_rapida(origen, destino)

    if len(recorrido) == 1:
        print(f"\nYa estas en {recorrido[0]}: 0 min.")
        return
    print(f"\nRuta mas rapida: {' -> '.join(recorrido)}")
    print("Tramos:")
    for a, b in zip(recorrido, recorrido[1:]):
        print(f"  {a} -> {b}: {g.adj[a][b]} min")
    print(f"Tiempo total: {minutos} min ({formatear_tiempo(minutos)})")


MENU = """
===== SISTEMA DE NAVEGACIÓN GPS =====
1. Ver todas las ciudades
2. Agregar nueva ruta
3. Consultar ruta más rápida
4. Salir
"""


def main():
    g = GrafoPonderado()
    cargar_datos_iniciales(g)
    acciones = {"1": opcion_ver_ciudades, "2": opcion_agregar_ruta,
                "3": opcion_consultar_ruta}

    while True:
        print(MENU)
        try:
            opcion = input("Elige una opcion: ").strip()
            if opcion == "4":
                print("¡Buen viaje!")
                break
            if opcion not in acciones:
                print("  ! Opción no valida. Elige 1, 2, 3 o 4.")
                continue
            acciones[opcion](g)
        except ErrorGPS as e:                 # errores esperados del sistema
            print(f"\n  ! {e}")
        except ValueError as e:
            print(f"\n  ! {e}")
        except (EOFError, KeyboardInterrupt):
            print("\nSaliendo del sistema...")
            break


if __name__ == "__main__":
    main()
