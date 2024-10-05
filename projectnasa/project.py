import pygame
import sys
import math
import random


pygame.init()

# Constants
WIDTH, HEIGHT = 1280, 720
CENTER_X, CENTER_Y = WIDTH // 2, HEIGHT // 2
SUN_RADIUS = 20
ASTEROID_RADIUS = 15
ASTEROID_SPEED = 2
FONT_SIZE = 36
ASTEROID_SPAWN_TIME = 1200  # Time in milliseconds between asteroid spawns

# Planet data
PLANET_DATA = {
    "Mercury": {"color": (169, 169, 169), "radius": 5, "speed": 0.04787, "distance": 40},
    "Venus": {"color": (255, 228, 196), "radius": 7, "speed": 0.03502, "distance": 75},
    "Earth": {"color": (0, 191, 255), "radius": 7, "speed": 0.02978, "distance": 105},
    "Mars": {"color": (255, 99, 71), "radius": 6, "speed": 0.02407, "distance": 145},
    "Jupiter": {"color": (255, 165, 0), "radius": 12, "speed": 0.01307, "distance": 240},
    "Saturn": {"color": (255, 228, 181), "radius": 11, "speed": 0.00969, "distance": 340},
    "Uranus": {"color": (135, 206, 235), "radius": 8, "speed": 0.00681, "distance": 480},
    "Neptune": {"color": (0, 0, 128), "radius": 8, "speed": 0.00543, "distance": 600},
}

# Initialize variables
planet_angles = {planet: 0 for planet in PLANET_DATA.keys()}
button_rect = pygame.Rect(CENTER_X - 50, HEIGHT - 100, 100, 50)
moving = False
game_over = False
asteroids = []
last_spawn_time = pygame.time.get_ticks()
score = 0

# Load images
BACKGROUND_IMAGE_PATH = "images/pexels-francesco-ungaro-998641.jpg" 
background_image = pygame.transform.scale(pygame.image.load(BACKGROUND_IMAGE_PATH), (WIDTH, HEIGHT))
crosshair_img = pygame.transform.scale(pygame.image.load("images/image-removebg-preview.png"), (40, 40))
asteroid_image = pygame.transform.scale(pygame.image.load("images/1950DA.png"), (30, 30))


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AsteroidMania")
font = pygame.font.Font(None, FONT_SIZE)


pygame.mouse.set_cursor((20, 20), crosshair_img)

def spawn_asteroid():
    angle = random.uniform(0, 2 * math.pi)
    x = int(CENTER_X + random.randint(200, 400) * math.cos(angle))
    y = int(CENTER_Y + random.randint(200, 400) * math.sin(angle))
    direction_angle = random.uniform(0, 2 * math.pi)  # Random angle for direction
    direction_x = math.cos(direction_angle) * ASTEROID_SPEED
    direction_y = math.sin(direction_angle) * ASTEROID_SPEED
    return {"x": x, "y": y, "direction_x": direction_x, "direction_y": direction_y}

def update_asteroid(asteroid):
    asteroid["x"] += asteroid["direction_x"]
    asteroid["y"] += asteroid["direction_y"]

def draw_asteroid(asteroid):
    screen.blit(asteroid_image, (asteroid["x"] - asteroid_image.get_width() // 2, asteroid["y"] - asteroid_image.get_height() // 2))

def update_planet(planet):
    planet_angles[planet] += PLANET_DATA[planet]["speed"]

def get_planet_position(planet):
    distance = PLANET_DATA[planet]["distance"]
    new_x = int(CENTER_X + distance * math.cos(planet_angles[planet]))
    new_y = int(CENTER_Y + distance * math.sin(planet_angles[planet]))
    return new_x, new_y

def draw_orbit(planet):
    distance = PLANET_DATA[planet]["distance"]
    pygame.draw.circle(screen, (255, 255, 255, 50), (CENTER_X, CENTER_Y), distance, 1)

def draw_button(text):
    pygame.draw.rect(screen, (0, 255, 0), button_rect)
    text_render = font.render(text, True, (0, 0, 0))
    text_rect = text_render.get_rect(center=button_rect.center)
    screen.blit(text_render, text_rect)

def draw_score():
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

def draw_instructions():
    instructions = font.render("Click on asteroids to destroy them!", True, (255, 255, 255))
    screen.blit(instructions, (10, HEIGHT - 50))

def draw_game_over():
    game_over_text = font.render("Game Over!", True, (255, 255, 255))
    restart_button_rect = pygame.Rect(CENTER_X - 50, CENTER_Y, 100, 50)
    restart_button_text = font.render("Try Again", True, (0, 0, 0))
    
    screen.blit(game_over_text, (CENTER_X - 80, CENTER_Y - 50))
    pygame.draw.rect(screen, (255, 0, 0), restart_button_rect)
    text_rect = restart_button_text.get_rect(center=restart_button_rect.center)
    screen.blit(restart_button_text, text_rect)
    
    return restart_button_rect

def reset_game():
    global asteroids, score, game_over, last_spawn_time, moving, button_text
    asteroids.clear()
    score = 0
    game_over = False
    moving = False  
    button_text = "Start" 
    last_spawn_time = pygame.time.get_ticks()  
    for planet in planet_angles.keys():
        planet_angles[planet] = 0  


running = True
button_text = "Start"

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(event.pos):
                moving = not moving  
                button_text = "Stop" if moving else "Start"
            if game_over:
                restart_button_rect = draw_game_over()
                if restart_button_rect.collidepoint(event.pos):
                    reset_game()  
            for asteroid in asteroids[:]:
                if math.dist((event.pos[0], event.pos[1]), (asteroid["x"], asteroid["y"])) < ASTEROID_RADIUS:
                    asteroids.remove(asteroid)
                    score += 1

    screen.blit(background_image, (0, 0))
    pygame.draw.circle(screen, (255, 204, 0), (CENTER_X, CENTER_Y), SUN_RADIUS)
    draw_button(button_text)
    draw_instructions()

    for planet in PLANET_DATA.keys():
        if moving:
            update_planet(planet)
        draw_orbit(planet)
        planet_x, planet_y = get_planet_position(planet)
        pygame.draw.circle(screen, PLANET_DATA[planet]["color"], (planet_x, planet_y), PLANET_DATA[planet]["radius"])

    
    if moving and pygame.time.get_ticks() - last_spawn_time > ASTEROID_SPAWN_TIME:
        asteroids.append(spawn_asteroid())
        last_spawn_time = pygame.time.get_ticks()

    if moving:
        for asteroid in asteroids[:]:
            update_asteroid(asteroid)  
            draw_asteroid(asteroid)

    draw_score()

   
    for asteroid in asteroids[:]:
        for planet in PLANET_DATA.keys():
            if math.dist((asteroid["x"], asteroid["y"]), get_planet_position(planet)) < PLANET_DATA[planet]["radius"]:
                game_over = True

    if game_over:
        draw_game_over()

    pygame.display.flip()
    pygame.time.delay(30)

# Quit Pygame
pygame.quit()
sys.exit()
