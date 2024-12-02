import pygame
import sys

# Inițializează Pygame
pygame.init()

# Dimensiunea ferestrei
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Obiect în mișcare")

# Culoarea de fundal
background_color = (0, 0, 0)  # Negru

# Culoarea obiectului
square_color = (255, 0, 0)  # Roșu

# Dimensiunea obiectului
square_size = 50

# Poziția inițială a obiectului
x = 100
y = 100
speed = 5

# Buclele de joc
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Mișcarea obiectului
    x += speed
    if x > screen_width - square_size or x < 0:
        speed = -speed  # Schimbă direcția când ajunge la margine

    # Umple ecranul cu fundalul
    screen.fill(background_color)

    # Desenează pătratul pe ecran
    pygame.draw.rect(screen, square_color, (x, y, square_size, square_size))

    # Actualizează fereastra
    pygame.display.flip()

    # Controlează viteza animației
    pygame.time.Clock().tick(60)  # 60 FPS
