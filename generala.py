class TurnoError(Exception):
    pass


class TablaPuntosError(Exception):
    pass

def calcular_repetidos(dados):
    repetidos = [0] * 6
    for dado in dados:
        index = dado - 1
        repetidos[index] += 1

    return repetidos


def buscar_repetido(dados, repetidos, cantidad_repetidos, estricto=False):
    encontre = False
    for repetido in repetidos:
        if repetido >= cantidad_repetidos:
            encontre = True
    return encontre

def buscar_repetido_full(dados, repetidos, cantidad_repetidos, estricto=False):
    encontre = False
    for repetido in repetidos:
        if repetido == cantidad_repetidos:
            encontre = True
    return encontre


def calcular_puntos(numero_lanzamiento, dados, juego):
    puntos = 0
    if juego == "escalera":
        dados.sort()
        if dados == [1, 2, 3, 4, 5] or dados == [2, 3, 4, 5, 6]:
            puntos = 20
            if numero_lanzamiento == 1:
                puntos += 5
    if juego == "generala":
        repetidos = calcular_repetidos(dados)
        if buscar_repetido(dados, repetidos, 5):
            puntos = 50
    elif juego == "poker":
        repetidos = calcular_repetidos(dados)
        if buscar_repetido(dados, repetidos, 4):
            puntos = 40
            if numero_lanzamiento == 1:
                puntos += 5
    elif juego == "full":
        repetidos = calcular_repetidos(dados)
        if buscar_repetido_full(dados, repetidos, 3) and buscar_repetido_full(dados, repetidos, 2):
            puntos = 30
            if numero_lanzamiento == 1:
                puntos += 5
    else:
        for dado in dados:
            if juego == str(dado):
                puntos += dado
    return puntos


class Jugador:
    pass


from random import randint


class Dados:
    def __init__(self, cantidad_dados):
        self._valores = [randint(1, 6) for _ in range(cantidad_dados)]

    @property
    def cantidad(self):
        return len(self._valores)

    @property
    def valores(self):
        return self._valores


class Turno:
    def __init__(self):
        self.numero_lanzamiento = 1
        self.dados_lanzados = Dados(5)
        self.dados_seguir = Dados(0)

    def guardar_dados(self, indices):
        dados_finales_ant = self.dados_finales
        self.dados_seguir = Dados(0)
        for indice in indices:
            self.dados_seguir.valores.append(dados_finales_ant[indice])
        self.siguiente_turno()

    def siguiente_turno(self):
        if(self.numero_lanzamiento >= 3):
            raise TurnoError("Límite de lanzamientos alcanzado")

        self.numero_lanzamiento += 1
        self.dados_lanzados = Dados(5 - self.dados_seguir.cantidad)

    def generala_servida(self):
        repetidos = calcular_repetidos(self.dados_finales)
        return buscar_repetido(self.dados_finales, repetidos, 5) and self.numero_lanzamiento == 1

    @property
    def dados_finales(self):
        return self.dados_lanzados.valores + self.dados_seguir.valores


class TablaPuntos:
    def __init__(self, cantidad_jugadores):
        self.cantidad_jugadores = cantidad_jugadores
        self._tabla = [  # lista
            {  # diccionario
                '1': None,
                '2': None,
                '3': None,
                '4': None,
                '5': None,
                '6': None,
                'escalera': None,
                'full': None,
                'poker': None,
                'generala': None,
                'generala_doble': None,
            }
            for _ in range(cantidad_jugadores)
        ]

    @property
    def estado_tabla(self):
        for jugada in self._tabla[-1].values():
            if jugada is None:
                return False
        return True  # Significa que la tabla del ultimo jugador esta llena

    def anotar(self, jugador, jugada, numero_lanzamiento, dados):
        if self._tabla[jugador][jugada] is None:
            puntos = calcular_puntos(numero_lanzamiento, dados, jugada)
            self._tabla[jugador][jugada] = puntos
        else:
            raise TablaPuntosError('jugada ya anotado!')


class Generala:
    def __init__(self, cantidad_jugadores):
        self.cantidad_jugadores = cantidad_jugadores
        self.esta_jugado = True
        self.jugador_esta_jugando = True
        self.jugador_actual = 0
        self.turno_actual = Turno()
        self.tabla_puntos = TablaPuntos(cantidad_jugadores)

    def siguiente_jugador(self):
        self.jugador_actual += 1
        self.jugador_actual = self.jugador_actual % self.cantidad_jugadores
        self.turno_actual = Turno()
        self.jugador_esta_jugando = True

    def anotar(self, jugada):
        try:
            self.tabla_puntos.anotar(
                self.jugador_actual,
                jugada,
                self.turno_actual.numero_lanzamiento,
                self.turno_actual.dados_finales,
            )
            if self.tabla_puntos.estado_tabla:
                self.esta_jugado = False
            else:
                self.siguiente_jugador()
            return "OK"
        except TablaPuntosError as e:
            return str(e)

    def dados_finales(self, dados_seguir):
        if dados_seguir == "ANOTAR" :
            self.jugador_esta_jugando = False
        else:
            if dados_seguir == "":
                list_int_dados_seguir = []
            else:
                list_dados_seguir = dados_seguir.split(sep=',')
                list_int_dados_seguir = [int(dado) for dado in list_dados_seguir]
            self.turno_actual.guardar_dados(list_int_dados_seguir)
            if self.turno_actual.numero_lanzamiento == 3:
                self.jugador_esta_jugando = False

    def victoria_instantanea(self):
        if self.turno_actual.generala_servida():
            self.jugador_esta_jugando = False
            self.esta_jugado = False
            return True
        else:
            return False

def main():
    cantidad_jugadores = int(input('Cantidad jugadores: '))
    juego = Generala(cantidad_jugadores)
    while juego.esta_jugado:
        if juego.victoria_instantanea():
                print("Tenes generala servida. ¡¡Ganaste!!")
                break
        else:
            while juego.jugador_esta_jugando:
                print('Jugador actual: {}'.format(juego.jugador_actual))
                print('\nLanzamiento nº: {}'.format(juego.turno_actual.numero_lanzamiento))
                print(juego.turno_actual.dados_finales)
                dados_seguir = input('Elija los dados con los que quiere seguir o presione enter para tirar todos los dados nuevamente. \n Para finalizar el turno escriba ANOTAR:\n')
                juego.dados_finales(dados_seguir)
            print('Jugador actual: {}'.format(juego.jugador_actual))
            print('\nLanzamiento nº: {}'.format(juego.turno_actual.numero_lanzamiento))
            print(juego.turno_actual.dados_finales)
            jugada = input('¿Que jugada quiere anotar?\n')
            print(juego.anotar(jugada))
            print(juego.tabla_puntos._tabla)


if __name__ == '__main__':
    main()