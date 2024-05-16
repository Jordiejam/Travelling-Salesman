import pygame
import sys
import random
from itertools import permutations
from math import factorial

def cities_permuter(cities:list[pygame.Vector2]):
    starting_city = random.choice(cities)
    rest_of_cities = cities.remove(starting_city)

    for cities_permutation in permutations(rest_of_cities):
        yield (starting_city) + cities_permutation

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

num_cities = random.randint(6, 14)
city_r = 10
cities = [pygame.Vector2(random.randint(0+city_r, WIDTH-city_r), random.randint(0+city_r, HEIGHT-city_r)) for _ in range(num_cities)]
shortest_route = float('inf')
best_perm = None

starting_city = cities[0]
perm_cities = cities[1:]
cities_perm = permutations(perm_cities)
total_perm = factorial(num_cities-1)

fps_average = []

def reset():
    global num_cities, cities, shortest_route, best_perm, cities_perm, total_perm, iteration, starting_city
    num_cities = random.randint(6, 12)
    cities = [pygame.Vector2(random.randint(0+city_r, WIDTH-city_r), random.randint(0+city_r, HEIGHT-city_r)) for _ in range(num_cities)]
    shortest_route = float('inf')
    best_perm = None

    starting_city = cities[0]
    perm_cities = cities[1:]
    cities_perm = permutations(perm_cities)
    total_perm = factorial(num_cities-1)

    iteration = 0
    

# Main game loop
running = True
iteration = 0
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                reset()

    # Game logic goes here
    
    if iteration < total_perm:

        for i in range(min(100, total_perm-iteration)):
            sum_dist = 0
            new_perm = next(cities_perm)
            new_perm = (starting_city, *new_perm)
            for city in new_perm:
                sum_dist += city.distance_to(new_perm[(new_perm.index(city)+1) % num_cities])
            
            if sum_dist < shortest_route:
                shortest_route = sum_dist
                best_perm = new_perm
            iteration += 1
        # print(f"{iteration}/{total_perm}: {sum_dist} ({clock.get_fps()})")
    
    percent_complete = f"{iteration / total_perm * 100:.4f}%" if iteration < total_perm else f"Best Route Achieved: {shortest_route:.0f} pixels"

    # Drawing code goes here
    screen.fill((0, 0, 0))  # Fill the screen with black

    for city in range(num_cities): # Render Routes
        pygame.draw.line(screen, (255, 255, 255), best_perm[city], best_perm[(city+1) % num_cities], city_r//2)
        if iteration < total_perm:
            pygame.draw.line(screen, "red", new_perm[city], new_perm[(city+1) % num_cities],1)

    for city in cities: # Render Cities
        colour = "limegreen" if city == starting_city else "white"
        pygame.draw.circle(screen, colour, city, city_r)

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
