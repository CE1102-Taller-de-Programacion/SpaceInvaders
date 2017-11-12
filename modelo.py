import json
import csv


def get_puntajes():
    with open("puntajes.json",  "r") as f:
        puntajes = json.load(fp=f)
    for key in puntajes:
        yield key, puntajes[key]


def get_jugadores():
    """
    :yield: Nombre de jugador
    Función iterable, en cada ciclo devuelve el nombre de un jugador
    """
    with open("jugadores.csv", "r", newline="") as f:
        file = csv.reader(f)
        file = next(file)
    for jugador in file:
        yield jugador


def set_puntajes(puntajes_dict):
    with open("puntajes.json", "w") as f:
        json.dump(obj=puntajes_dict, fp=f, indent=True, separators=True)

    with open("jugadores.csv", "w"):
        for i in puntajes_dict:
            f.write(s=puntajes_dict[i]["nombre"]+",")


def insertar_pungaje(jugador):
    pass
