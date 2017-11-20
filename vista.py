import pygame
import threading
import inputbox


class Juego:
    def __init__(self, controlador, defensor, atacantes):
        self.controlador = controlador
        self.defensor = defensor
        self.atacantes = atacantes

        # Colores en RGB
        self.NEGRO = (0, 0, 0)
        self.BLANCO = (255, 255, 255)
        self.ROJO = (237, 74, 60)
        self.ANARANJADO = (255, 136, 0)
        self.GRIS = (33, 33, 33)
        self.VERDE = (0, 200, 81)
        self.AZUL = (0, 153, 204)

        self.puntaje = 0

        self.reloj = pygame.time.Clock()
        self.FPS = 60

        self.pantalla_completa = False
        self.ancho, self.altura = 1152, 648
        self.ventana = pygame.display.set_mode((self.ancho, self.altura))
        pygame.display.set_caption("Space Invaders")
        icono = pygame.image.load("imagenes/icon.png")
        pygame.display.set_icon(icono)

        atacantes_x, atacantes_y = 20, 60
        for i in range(len(self.atacantes)):
            for j in range(len(self.atacantes[0])):
                self.atacantes[i][j].pos["x"] = atacantes_x
                self.atacantes[i][j].pos["y"] = atacantes_y
                atacantes_x += 60
            atacantes_x = 20
            atacantes_y += 50

        # Definen tamaños de Surfaces
        self.tamano_defensor = 60
        self.tamano_atacante = 40
        self.tamano_disparo_x = 10
        self.tamano_disparo_y = 20

        # Velocidad inicial de atacantes y defensor
        self.velocidad_atacantes = 2
        self.direccion_atacantes_x = 2
        self.direccion_atacantes_y = 0

        self.disparos_defensor = []
        self.disparos_atacantes = []

        # Crear surfaces de defensor y atacantes
        defensor = pygame.image.load("imagenes/defensor.png")
        self.defensor = pygame.transform.scale(defensor, (self.tamano_defensor, self.tamano_defensor))
        atacante = pygame.image.load("imagenes/atacante.png")
        self.atacante = pygame.transform.scale(atacante, (self.tamano_atacante, self.tamano_atacante))
        fondo = pygame.image.load("animaciones/fondo2.gif")
        self.fondo = pygame.transform.scale(fondo, (self.ancho, self.altura))

        self.defensor_x = self.ancho // 2 - self.tamano_defensor
        self.defensor_y = round(self.altura * (3 / 4))
        self.defensor_x_cambio = 0
        self.defensor_y_cambio = 0

        pygame.init()
        pygame.joystick.init()
        self.joystick_count = pygame.joystick.get_count()
        self.joysticks = []
        for i in range(self.joystick_count):
            joystick = pygame.joystick.Joystick(i)
            joystick.init()
            self.joysticks.append(joystick)
        self.menu()

    def menu(self):
        ir_config = False
        salir_juego = False
        texto_bienvenida = pygame.font.SysFont("Roboto", 90)
        texto_comenzar = pygame.font.SysFont("Roboto", 50)
        bienvenida = texto_bienvenida.render("¡Bienvenido a Space Invaders!", True, self.VERDE)
        comenzar = texto_comenzar.render("Oprima cualquier tecla / botón para comenzar", True, self.AZUL)

        fondo = pygame.image.load("imagenes/fondo2.png")
        fondo = pygame.transform.scale(fondo, (self.ancho, self.altura))

        while not ir_config and not salir_juego:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    salir_juego = True
                if event.type == pygame.JOYBUTTONDOWN:
                    ir_config = True
                if event.type == pygame.KEYDOWN:
                    ir_config = True
            self.ventana.fill(self.GRIS)
            self.ventana.blit(fondo, (0, 0))
            self.ventana.blit(bienvenida, (150, self.altura // 2 - 150))
            self.ventana.blit(comenzar, (200, self.altura // 2))
            pygame.display.update()
            self.reloj.tick(self.FPS)
        if ir_config:
            self.config()
        else:
            pygame.quit()

    def config(self):
        comenzar_juego = False
        salir_juego = False

        fondo = pygame.image.load("imagenes/fondo2.png")
        fondo = pygame.transform.scale(fondo, (self.ancho, self.altura))

        seleccionar = pygame.font.SysFont("Roboto", 40)
        seleccionar = seleccionar.render("Seleccione nombre de jugador", True, self.AZUL)
        crear = pygame.font.SysFont("Roboto", 20)
        crear = crear.render("Si el jugador ya existe, será cargado automáticamente", True, self.ROJO)

        while not comenzar_juego and not salir_juego:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    salir_juego = True

            self.ventana.fill(self.GRIS)
            self.ventana.blit(fondo, (0, 0))
            self.ventana.blit(seleccionar, (375, 200))
            self.ventana.blit(crear, (400, 240))
            pygame.display.update()
            self.reloj.tick(self.FPS)

        if comenzar_juego:
            pass
        else:
            pygame.quit()

    def juego_terminado(self):
        ir_menu = False
        salir_juego = False
        texto1 = pygame.font.SysFont("Roboto", 100)
        texto2 = pygame.font.SysFont("Roboto", 50)
        final = texto1.render("¡Partida Terminada!", True, self.AZUL)
        puntaje_partida = texto2.render("Puntaje final: {}".format(self.puntaje), True, self.VERDE)
        while not ir_menu and not salir_juego:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    salir_juego = True
                if event.type == pygame.KEYDOWN:
                    ir_menu = True
            self.ventana.fill(self.GRIS)
            self.ventana.blit(final, (250, 250))
            self.ventana.blit(puntaje_partida, (450, 350))
            pygame.display.update()
            self.reloj.tick(self.FPS)
        if ir_menu:
            pass
        else:
            pygame.quit()

    def principal(self):
        """
        Loop principal del juego
        """
        pygame.mixer.init()
        texto = pygame.font.SysFont("Roboto", 25)
        # Determina si el jugador a perdido la partida
        juego_terminado = False
        # Determina si se debe salir del juego por completo
        salir_juego = False

        while not juego_terminado and not salir_juego:
            puntaje = texto.render("Puntaje: {}".format(self.puntaje), True, self.BLANCO)
            # Variable creada para determinar si una nave dada debe disparar en un cuadro particular
            atacante_dispara = self.controlador.get_random_senal()

            # Devuelve todos los eventos que ocurran
            for event in pygame.event.get():
                # Sale de juego
                if event.type == pygame.QUIT:
                    salir_juego = True

                # Acciones en caso de presionar botón en joystick
                if event.type == pygame.JOYBUTTONDOWN:
                    # Dispara si se presiona el botón 0 del joystick
                    if self.boton_pres(0):
                        self.disparar()

                # Acciones en caso de presionar flecha en joystick
                if event.type == pygame.JOYHATMOTION:
                    if self.flecha_pres() == (1, 1):
                        self.defensor_x_cambio = 5
                        self.defensor_y_cambio = -5
                    elif self.flecha_pres() == (-1, -1):
                        self.defensor_x_cambio = -5
                        self.defensor_y_cambio = 5
                    elif self.flecha_pres() == (1, -1):
                        self.defensor_x_cambio = 5
                        self.defensor_y_cambio = 5
                    elif self.flecha_pres() == (-1, 1):
                        self.defensor_x_cambio = -5
                        self.defensor_y_cambio = -5
                    elif self.flecha_pres() == (0, 0):
                        self.defensor_x_cambio = 0
                        self.defensor_y_cambio = 0
                    elif self.flecha_pres() == (0, -1):
                        self.defensor_x_cambio = 0
                        self.defensor_y_cambio = 5
                    elif self.flecha_pres() == (0, 1):
                        self.defensor_x_cambio = 0
                        self.defensor_y_cambio = -5
                    elif self.flecha_pres() == (-1, 0):
                        self.defensor_x_cambio = -5
                        self.defensor_y_cambio = 0
                    elif self.flecha_pres() == (1, 0):
                        self.defensor_x_cambio = 5
                        self.defensor_y_cambio = 0

                # Acciones en caso de presionar tecla
                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_q:
                        juego_terminado = True

                    # Entra en modo de pantalla completa al presionar "k"
                    if event.key == pygame.K_f:
                        if not self.pantalla_completa:
                            self.ancho, self.altura = 1280, 720
                            self.ventana = pygame.display.set_mode((self.ancho, self.altura),
                                                                   pygame.FULLSCREEN)
                            self.pantalla_completa = True
                        else:
                            self.ancho, self.altura = 1152, 648
                            self.ventana = pygame.display.set_mode((self.ancho, self.altura))
                            self.pantalla_completa = False
                    # Mover nave defensora a la izquierda
                    if event.key == pygame.K_LEFT:
                        self.defensor_x_cambio = -5
                    # Mover nave defensora a la derecha
                    elif event.key == pygame.K_RIGHT:
                        self.defensor_x_cambio = 5
                    # Mover nave defensora hacia arriba
                    if event.key == pygame.K_UP:
                        self.defensor_y_cambio = -5
                    # Mover nave defensora hacia abajo
                    elif event.key == pygame.K_DOWN:
                        self.defensor_y_cambio = 5
                    # Nave defensora dispara munición
                    if event.key == pygame.K_SPACE:
                        self.disparar()

                # Acciones al liberar una tecla
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        self.defensor_x_cambio = 0
                    if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        self.defensor_y_cambio = 0

            # Condiciones evitan que la nave se salga del area de la pantalla
            if 0 <= self.defensor_x <= self.ancho - self.tamano_defensor:
                self.defensor_x += self.defensor_x_cambio
            elif self.defensor_x <= 0:
                self.defensor_x = 1
            else:
                self.defensor_x = self.ancho - self.tamano_defensor - 1
            if 0 <= self.defensor_y <= self.altura - self.tamano_defensor:
                self.defensor_y += self.defensor_y_cambio
            elif self.defensor_y <= 0:
                self.defensor_y = 1
            else:
                self.defensor_y = self.altura - self.tamano_defensor - 1

            self.ventana.fill(self.NEGRO)
            self.ventana.blit(self.fondo, [0, 0])
            self.ventana.blit(puntaje, (20, 20))

            # Dibuja defensor
            self.ventana.blit(self.defensor, (self.defensor_x, self.defensor_y))

            # Dibuja todos los disparos en self.disparos_defensor
            for pew in self.disparos_defensor:
                if pew["y"] > 0:
                    pew["y"] -= 8
                    pygame.draw.rect(self.ventana, self.ROJO,
                                     [pew["x"], pew["y"], self.tamano_disparo_x, self.tamano_disparo_y])
                else:
                    self.disparos_defensor.remove(pew)

            # Dibuja todos los disparos en self.disparos_atacantes
            for pew in self.disparos_atacantes:
                if pew["y"] < self.altura:
                    pew["y"] += 8
                    pygame.draw.rect(self.ventana, self.ANARANJADO,
                                     [pew["x"], pew["y"], self.tamano_disparo_x, self.tamano_disparo_y])
                else:
                    self.disparos_atacantes.remove(pew)

            # Ciclo para manejar acciones de atacanes dentro de matriz self.atacantes
            for fila in range(len(self.atacantes)):
                for atacante in range(len(self.atacantes[0])):
                    for pew in self.disparos_defensor:
                        # Determina si alguno de los disparos colisiona con un atacante
                        # De ser así, el atacante muere y se suman 100 puntos
                        if self.colision(range(pew["x"], pew["x"] + self.tamano_disparo_x),
                            range(pew["y"], pew["y"] + self.tamano_disparo_y),
                            range(round(self.atacantes[fila][atacante].pos["x"]),
                                  round(self.atacantes[fila][atacante].pos["x"] + self.tamano_atacante)),
                            range(self.atacantes[fila][atacante].pos["y"] + self.direccion_atacantes_y,
                                  self.atacantes[fila][atacante].pos["y"] + self.tamano_atacante +
                                          self.direccion_atacantes_y))\
                                and self.atacantes[fila][atacante].vida:

                            self.disparos_defensor.remove(pew)
                            self.atacantes[fila][atacante].vida = False
                            self.puntaje += 100
                            pygame.mixer.music.load("audio/invaderkilled.wav")
                            pygame.mixer.music.play()

                    # De tener vida el atacante, lo mueve
                    if self.atacantes[fila][atacante].vida:
                        self.atacantes[fila][atacante].pos["x"] += self.direccion_atacantes_x
                        self.ventana.blit(self.atacante, (self.atacantes[fila][atacante].pos["x"],
                                                          self.atacantes[fila][atacante].pos["y"] +
                                                          self.direccion_atacantes_y))

                        if self.atacantes[fila][atacante].senal_disparo == atacante_dispara:
                            self.disparos_atacantes.append({"x": self.atacantes[fila][atacante].pos["x"] +
                                                                 self.tamano_atacante//2,
                                                           "y": self.atacantes[fila][atacante].pos["y"] +
                                                                self.direccion_atacantes_y + self.tamano_disparo_y})

                # Determina la próxima dirección de los atacantes
                se_paso = False
                for fila in range(len(self.atacantes)):
                    for columna in range(len(self.atacantes)):
                        # Determina si un atacante tiene vida y se paso del ancho del area de pantalla
                        # En caso de ser así, invierte la dirección en x, aumenta y, y aumenta la velocidad
                        if self.atacantes[columna][fila].vida and \
                                self.atacantes[columna][fila].pos["x"] <= 0:
                            self.direccion_atacantes_x = self.velocidad_atacantes
                            se_paso = True
                        elif self.atacantes[columna][len(self.atacantes[0]) - 1 - fila].vida and \
                                self.atacantes[columna][len(self.atacantes[0]) - 1 - fila].pos["x"] \
                                    >= self.ancho - self.tamano_atacante:
                            self.velocidad_atacantes += .3
                            self.direccion_atacantes_x = -self.velocidad_atacantes
                            self.direccion_atacantes_y += 10
                            se_paso = True
                        if se_paso:
                            break
                    if se_paso:
                        break

            pygame.display.update()
            # Cuadros por segundo del juego
            self.reloj.tick(self.FPS)
        if juego_terminado:
            self.juego_terminado()
        elif salir_juego:
            pygame.quit()

    def disparar(self):
        """
        Añade un disparo a self.disparos_defensor
        """
        self.disparos_defensor.append({"x": self.defensor_x + 25,
                              "y": self.defensor_y - 20})

    def colision(self, rangex1, rangey1, rangex2, rangey2):
        """
        :param rangex1: rango de x en objeto 1
        :param rangey1: rango de y en objeto 1
        :param rangex2: rango de x en objeto 2
        :param rangey2: rango de y en objeto 2
        :return: bool que determina si la colisión ocurrió
        """
        en_x = False
        en_y = False
        for i in rangex1:
            if i in rangex2:
                en_x = True
        if not en_x:
            return False
        for i in rangey1:
            if i in rangey2:
                en_y = True
        return en_x and en_y

    def boton_pres(self, boton):
        """
        :param boton: boton que se desea conocer su estado
        :return: bool, indica si el boton esta siendo presionado en el joystick
        """
        es_presionado = False
        for i in range(self.joystick_count):
            if self.joysticks[i].get_numbuttons() > 0:
                if self.joysticks[i].get_button(boton):
                    es_presionado = True
                    break
        return es_presionado

    def flecha_pres(self):
        """
        :return: tupla de ints, indica las posiciones de las flechas en el joystick
        """
        for i in range(self.joystick_count):
            if self.joysticks[i].get_numhats() > 0:
                return self.joysticks[i].get_hat(0)
