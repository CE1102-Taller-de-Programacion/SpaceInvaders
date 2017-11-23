import vista as vi
import modelo as md
import threading
import random

# Antes de correr, determina si tiene los archivos necesarios para no parar hasta llegar runtime.
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
    """
    Clase controlador que crea instancia de clase juego y es capaz de comunicar vista con modelo y viceversa.
    """
    def __init__(self, num_atacantes):
        # Numero de atacantes que se generaran en una matriz
        self.num_atacantes = num_atacantes
        self.atacantes = self.generar_atacantes()

        # Objeto en memoria de Juego
        self.vista = vi.Juego

        # Creación de la instancia de Juego dentro de su propio hilo.
        self.crear_juego = threading.Thread(target=self.principal)
        self.crear_juego.start()

    def principal(self):
        """
        Genera una instancia de Juego, encontrado en vista.
        """
        self.vista(self, Defensor(), self.atacantes)

    def generar_atacantes(self, num_atacantes=None):
        """
        :return: array de Atacante(s)
        Crea la cantidad de instancias de Atacante según self.num_atacantes y los ordena en una
        matriz.
        """
        if num_atacantes:
            self.num_atacantes = num_atacantes
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

    def get_jugadores(self):
        """
        :return: Lista de strings
        Obtiene una lista con los nombres de los jugadores existentes por medio de modelo.
        """
        return md.get_jugadores()

    def get_puntajes(self):
        """
        :yield: tupla de string y diccionario.
        Función iterable que en cada ciclo devuelve el nombre de un jugador y su puntaje.
        """
        for puntaje in md.get_puntajes():
            yield puntaje

    def get_random_senal(self, alto):
        """
        :param alto: alto del range a producir
        :return: int
        Función que devuelve int 0 < x < alto, donde alto es mayor a 200.
        """
        if alto < 200:
            alto = 200
        return random.randint(0, alto)

    def generar_jugador(self, nombre, record=None):
        """
        :param nombre: string, nombre del jugador
        :param record: int, record del jugador
        :return: Instancia Jugador con parámetros indicados.
        """
        return Jugador(nombre, record)

    def guardar_nuevo(self, jugador):
        """
        :param jugador: Jugador
        Guarda un jugador, previamente no existente, a los datos guardados.
        """
        md.insertar_puntaje_nuevo(jugador)

    def guardar_existante(self, jugador):
        """
        :param jugador: Jugador
        Actualiza un jugador, existente, en los datos guardados.
        """
        md.actaulizar_puntaje(jugador)


class Jugador:
    """
    Objeto que representa un jugador particular.
    """
    def __repr__(self):
        return "Jugador llamado {}, {} es su mayor puntaje".format(self.nombre, self.record)

    def __len__(self):
        return self.record

    def __init__(self, nombre, record=None):
        """
        :param nombre: string, nombre del jugador.
        :param record: string, record del jugador.
        """
        self.nombre = nombre
        if record:
            self.record = record
        else:
            self.record = 0


class Nave:
    """
    Objeto subclase que representa una nave particular.
    """
    def __init__(self):
        """
        Inicializa la nava con la posición por defecto y con vida.
        """
        self.pos = {"x": 0, "y": 0}
        self.vida = True

    def morir(self):
        """
        Cambia vida a falso, si esta es verdadera.
        """
        if self.vida:
            self.vida = False


class Atacante(Nave):
    """
    Objeto que representa una nava de atacante particular.
    """
    def __init__(self, estado=None):
        """
        :param estado: string, estado inicial del atacante
        Inicializa la subclase heredada y determina su señal de disparo.
        """
        super().__init__()
        if not estado:
            self.estado = "activo"
        else:
            self.estado = estado

        self.senal_disparo = random.randint(0, 200)

    def desprender(self):
        pass


class Defensor(Nave):
    """
    Objeto que representa una nave defensora particular.
    """
    def __init__(self):
        super().__init__()


if __name__ == "__main__":
    Controlador(30)
