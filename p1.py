import pygame
import sys
import random

# Inicialización de Pygame
pygame.init()

# Configuración de pantalla
WIDTH, HEIGHT = 800, 600
CELL_SIZE = 40
ROWS, COLS = HEIGHT // CELL_SIZE, WIDTH // CELL_SIZE
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Laberinto con Ratón y Plantas Carnívoras")

# Cargar imágenes
background_image = pygame.Surface((CELL_SIZE, CELL_SIZE))
background_image.fill((255, 255, 255))  # Fondo blanco para las celdas vacías
mouse_image = pygame.image.load("./img/mouse.png")
mouse_image = pygame.transform.scale(mouse_image, (CELL_SIZE, CELL_SIZE))
ghost_image = pygame.image.load("./img/ghost.png")
ghost_image = pygame.transform.scale(ghost_image, (CELL_SIZE, CELL_SIZE))

# Definir el laberinto como una lista de filas, donde 1 representa una pared y 0 representa un camino
laberinto = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

# Tamaño y posición del ratón
mouse_x, mouse_y = WIDTH // 2, HEIGHT // 2

# Tamaño y posición de las plantas carnívoras (fantasmas)
ghost_size = CELL_SIZE
ghosts = [(random.randint(0, COLS - 1) * CELL_SIZE, random.randint(0, ROWS - 1) * CELL_SIZE) for _ in range(3)]
ghost_speed = 2

def draw_laberinto():
    for y, row in enumerate(laberinto):
        for x, cell in enumerate(row):
            if cell == 1:
                screen.blit(background_image, (x * CELL_SIZE, y * CELL_SIZE))

def draw_objects():
    # Dibujar laberinto
    draw_laberinto()

    # Dibujar ratón
    screen.blit(mouse_image, (mouse_x, mouse_y))

    # Dibujar plantas carnívoras (fantasmas)
    for ghost in ghosts:
        screen.blit(ghost_image, ghost)

# Reloj para controlar la velocidad de actualización
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    # Movimiento del ratón con las teclas de flecha
    mouse_x += (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * 5
    mouse_y += (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * 5

    # Limpiar la pantalla
    screen.fill((255, 255, 255))

    # Dibujar objetos en pantalla
    draw_objects()

    # Actualizar la pantalla
    pygame.display.flip()

    # Controlar la velocidad de actualización
    clock.tick(30)