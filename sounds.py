import pygame

pygame.init()
pygame.mixer.init()


def musica_principal():
    pygame.mixer.music.load("audio/spaceinvaders1.mpeg")
    pygame.mixer.music.play()
