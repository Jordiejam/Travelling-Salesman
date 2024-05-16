# Hopcratft-Karp Algorithm

import pygame
import sys
import random
from itertools import permutations
from math import factorial

# Initialize Pygame
pygame.init()

# Constants for the screen dimensions
WIDTH = 1920/1.5
HEIGHT = 1080/1.5

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
font = pygame.font.SysFont(None, 48)
clock = pygame.time.Clock()
pygame.display.set_caption('The Travelling Salesman')

# Init Vars

num_cities = 12
city_r = 5
cities = [pygame.Vector2(random.randint(0+city_r, WIDTH-city_r), random.randint(0+city_r, HEIGHT-city_r)) for _ in range(num_cities)]
shortest_route = float('inf')
best_perm = None

cities_perm = permutations(cities) # use next to get the next permutation to save from calculating all of them at the start
total_perm = factorial(num_cities)

fps_average = []

# Main game loop
running = True
iteration = 0
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Game logic goes here
    
    if iteration < total_perm:

        for i in range(min(100, total_perm-iteration)):
            sum_dist = 0
            new_perm = next(cities_perm)
            for city in new_perm:
                sum_dist += city.distance_to(new_perm[(new_perm.index(city)+1) % num_cities])
            
            if sum_dist < shortest_route:
                shortest_route = sum_dist
                best_perm = new_perm
            iteration += 1
        print(f"{iteration}/{total_perm}: {sum_dist} ({clock.get_fps()})")
    
    percent_complete = f"{iteration / total_perm * 100:.4f}%" if iteration < total_perm else f"Best Route Achieved: {shortest_route}"

    # Drawing code goes here
    screen.fill((0, 0, 0))  # Fill the screen with black

    for city in cities: # Render Cities
        pygame.draw.circle(screen, (255, 255, 255), city, city_r)
    
    for city in range(num_cities): # Render Routes
        # if iteration < total_perm:
        #     pygame.draw.line(screen, "red", new_perm[city], new_perm[(city+1) % num_cities],1)
        pygame.draw.line(screen, (255, 255, 255), best_perm[city], best_perm[(city+1) % num_cities], city_r//2)


    screen.blit(font.render(percent_complete, True, (255, 255, 255)), (10, 10))

    if len(fps_average) > 3000:
        fps_average.pop(0)
    fps_average.append(clock.get_fps())
    average_fps = sum(fps_average)/len(fps_average)

    screen.blit(font.render(f"FPS: {average_fps:.1f}", True, (255, 255, 255)), (10, 50))
    
    #iteration += 1

    # Update the display
    pygame.display.flip()

    # Maintain a 60 frames per second rate
    clock.tick(float('inf'))

# Clean up and quit
pygame.quit()
sys.exit()
