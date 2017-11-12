import pygame

"""
# pygame.diplay.flip() # updates entire surface, all at once
"""
"""
 pygame.display.update()  only updates the areas you tell in *args you want
                        # it to update
                        
pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
joysticks[-1].init()
"""
pygame.init()

white = (255, 255, 255)
black = (0, 0, 0)

gameDisplay = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Slither")
jugador = pygame.image.load("ship.png")
jugador = pygame.transform.scale(jugador, (100, 100))
gameExit = False

lead_x = 300
lead_y = 300
lead_x_change = 0

clock = pygame.time.Clock()

while not gameExit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameExit = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                lead_x_change = -5
            if event.key == pygame.K_RIGHT:
                lead_x_change = 5
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                lead_x_change = 0
    lead_x += lead_x_change

    gameDisplay.fill(white)
    pygame.draw.rect(gameDisplay, black, [lead_x, lead_y, 10, 100])
    gameDisplay.blit(jugador, (lead_x, lead_y))
    pygame.display.update()
    clock.tick(60)

pygame.quit()
quit()
