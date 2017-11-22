import vista as vi
import modelo as md
import threading
import random

archivo = None
try:
    archivo = open(file="puntajes.json", mode="r")
except FileNotFoundError:
    print("Error, no se encontró archivo puntajes.json")
    raise FileNotFoundError
else:
    archivo.close()
try:
    archivo = open(file="jugadores.csv", mode="r")
except FileNotFoundError:
    print("Error, no se encontró archivo jugadores.csv")
    raise FileNotFoundError
else:
    archivo.close()


class Controlador:
    def __init__(self, num_atacantes):
        self.num_atacantes = num_atacantes
        self.atacantes = self.generar_atacantes()
        self.vista = vi.Juego

        self.crear_juego = threading.Thread(target=self.principal)
        self.crear_juego.start()

    def principal(self):
        """
        Genera una instancia de vista, donde se encuentra el juego.
        """
        self.vista(self, Defensor(), self.atacantes)

    def generar_atacantes(self):
        """
        :return: array de Atacante(s)
        Crea la cantidad de instancias de Atacante según self.num_atacantes y los ordena en una
        matriz.
        """
        result = [[]]
        j = 0
        for i in range(self.num_atacantes):
            if not i % 10 == 0 or i == 0:
                result[j] += [Atacante(100)]
            else:
                j += 1
                result += [[]]
                result[j] += [Atacante(100)]
        return result

    def crear_jugador(self):
        pass

    def get_jugadores(self):
        return md.get_jugadores()

    def get_puntajes(self):
        for puntaje in md.get_puntajes():
            yield puntaje

    def get_random_senal(self, alto):
        if alto < 200:
            alto = 200
        return random.randint(0, alto)

    def generar_jugador(self, nombre, record=None):
        return Jugador(nombre, record)

    def guardar_nuevo(self, jugador):
        md.insertar_puntaje_nuevo(jugador)

    def guardar_existante(self, jugador):
        md.actaulizar_puntaje(jugador)


class Jugador:
    def __repr__(self):
        return "Jugador llamado {}, {} es su mayor puntaje".format(self.nombre, self.record)

    def __len__(self):
        return self.record

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.guardar_record()

    def __init__(self, nombre, record=None):
        self.nombre = nombre
        if record:
            self.record = record
        else:
            self.record = 0

    def get_record(self):
        return self.record

    def set_record(self, puntaje):
        self.record = puntaje

    def guardar_record(self):
        es_top5 = False
        es_record = record_top5(self)
        if es_record == 1:
            es_top5 = True
        elif es_record == 0:
            pass
        else:
            pass
        return es_top5


def record_top5(jugador):
    records = md.get_puntajes()
    es_top5 = -1
    i = 0
    for j in records:
        i += 1
        if records[j]["record"] < jugador.record:
            if i <= 5:
                es_top5 = 1
            else:
                es_top5 = 0
    return es_top5


class Nave:
    def __init__(self):
        self.pos = {"x": 0, "y": 0}
        self.vida = True

    def morir(self):
        if self.vida:
            self.vida = False


class Atacante(Nave):
    def __init__(self, estado=None):
        super().__init__()
        if not estado:
            self.estado = "activo"
        else:
            self.estado = estado
        self.senal_disparo = random.randint(0, 200)

    def desprender(self):
        pass


class Defensor(Nave):
    def __init__(self):
        super().__init__()


if __name__ == "__main__":
    Controlador(30)
