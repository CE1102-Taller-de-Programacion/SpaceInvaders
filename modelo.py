import json
import csv


def get_jugadores():
    """
    :return: Lista con nombres de jugadores
    """
    with open("jugadores.csv", "r", newline="") as f:
        file = csv.reader(f)
        file = next(file)
        return file


def get_puntajes():
    """
    :yield: tupla con nombre de jugador y su puntaje.
    Función iterable, en cada ciclo devuelve la tupla de un jugador particular
    """
    with open("puntajes.json",  "r") as f:
        puntajes = json.load(fp=f)
    for key in puntajes:
        yield key, puntajes[key]


def actaulizar_puntaje(jugador):
    """
    :param jugador: diccionario con nombre de jugador y su puntaje.
    Actualiza el record de un jugador ya existente guardado en puntajes.json.
    """
    with open("puntajes.json", "r") as f:
        temp = json.load(fp=f)
    for i in temp:
        if i == jugador.nombre:
            temp[i]["puntaje"] = jugador.record
    temp_lista = []
    for subdicc in temp:
        temp_lista.append({subdicc: temp[subdicc]})
    result = {}
    pos = 1
    puntaje_temp = 0
    largo = len(temp_lista)
    while largo != len(result):
        for i in temp_lista:
            for key in i:
                if i[key]["puntaje"] >= puntaje_temp:
                    temp_dict = i
                    nombre = key
                    puntaje_temp = i[key]["puntaje"]
        puntaje_temp = 0
        temp_lista.remove(temp_dict)
        temp_dict[nombre]["pos"] = pos
        result[nombre] = temp_dict[nombre]
        pos += 1
    with open("puntajes.json", "w") as f:
        json.dump(obj=result, fp=f)


def insertar_puntaje_nuevo(jugador):
    """
    :param jugador: diccionario con nombre de jugador y su puntaje.
    General un nuevo jugador, de manera que se inserta en jugadores.csv y puntajes.json.
    """
    with open("jugadores.csv", "r", newline="") as f:
        temp = csv.reader(f)
        temp = next(temp)
        temp.append(jugador.nombre)
    with open("jugadores.csv", "w") as f:
        escribir = csv.writer(f)
        escribir.writerow(temp)
    dicc = {jugador.nombre: {"pos": 0, "puntaje": jugador.record}}
    with open("puntajes.json") as f:
        temp = json.load(fp=f)
    temp_lista = [dicc]
    for subdicc in temp:
        temp_lista.append({subdicc: temp[subdicc]})
    result = {}
    pos = 1
    puntaje_temp = 0
    largo = len(temp_lista)
    while largo != len(result):
        for i in temp_lista:
            for key in i:
                if i[key]["puntaje"] >= puntaje_temp:
                    temp_dict = i
                    nombre = key
                    puntaje_temp = i[key]["puntaje"]
        puntaje_temp = 0
        temp_lista.remove(temp_dict)
        temp_dict[nombre]["pos"] = pos
        result[nombre] = temp_dict[nombre]
        pos += 1
    with open("puntajes.json", "w") as f:
        json.dump(obj=result, fp=f)
