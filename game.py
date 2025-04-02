# # game.py
# # Purpose: 2D car game with scrolling road (image-based), styled player car (sprite), and traffic

# import pygame               # Pygame for game development
# import random               # Random for traffic spawning

# # Initialize Pygame
# pygame.init()

# # Set up the game window
# WIDTH = 800                 # Screen width
# HEIGHT = 900                # Screen height
# screen = pygame.display.set_mode((WIDTH, HEIGHT))
# pygame.display.set_caption("Face-Controlled Car Game")
# clock = pygame.time.Clock() # Control game speed

# # Colors
# BLACK = (0, 0, 0)           # Background

# # Load and scale image assets
# player_car_img = pygame.image.load("player_car.png").convert_alpha()  # Load player car sprite
# player_car_img = pygame.transform.scale(player_car_img, (50, 80))     # Scale to 50x80 pixels
# road_tile_img = pygame.image.load("road_v.png").convert_alpha()       # Load road tile image (already 800x600)

# # Load traffic car images (2.png through 6.png)
# traffic_car_images = []
# for i in range(2, 7):  # From 2 to 6
#     img = pygame.image.load(f"{i}.png").convert_alpha()  # Load each traffic car sprite
#     img = pygame.transform.scale(img, (50, 80))          # Scale to 50x80 pixels
#     traffic_car_images.append(img)

# # Player car properties (using Rect for collision detection)
# player_car = pygame.Rect(WIDTH // 2 - 25, HEIGHT - 100, 50, 80)  # Positioned near bottom
# player_speed = 0            # Player's vertical speed (positive = up, negative = down)
# MAX_SPEED = 10              # Maximum speed (upward)
# MIN_SPEED = -5              # Minimum speed (downward)
# ACCELERATION = 0.5          # How much speed increases per frame when accelerating
# DECELERATION = 0.3          # How much speed decreases per frame when decelerating

# # Road properties
# road_y = 0                  # Starting position of road tile
# BASE_ROAD_SPEED = 5         # Base speed of road scrolling
# MIN_ROAD_SPEED = -2         # Minimum road speed (allow slight reverse when braking)
# road_speed = BASE_ROAD_SPEED  # Actual road speed, influenced by player speed

# # Traffic properties
# traffic = []
# TRAFFIC_SPAWN_RATE = 50     # Frames between spawns
# traffic_counter = 0
# last_lane = None            # Track the last lane used to avoid consecutive spawns

# # Define lane centers for four lanes (based on 800px width, 50px car width)
# LANE_CENTERS = [200, 310, 460, 580]  # Centers of four lanes

# # Define road boundaries for player car (to stay off footpaths)
# ROAD_LEFT_BOUNDARY = 130    # Left edge of the road (after footpath)
# ROAD_RIGHT_BOUNDARY = 600   # Right edge of the road (before footpath, adjusted for car width)

# # Game loop
# running = True
# while running:
#     # Handle events
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
    
#     # Keyboard controls
#     keys = pygame.key.get_pressed()
#     # Horizontal movement (left/right) with road boundaries
#     if keys[pygame.K_LEFT] and player_car.x > ROAD_LEFT_BOUNDARY:
#         player_car.x -= 5       # Move car left, but not past the left road boundary
#     if keys[pygame.K_RIGHT] and player_car.x < ROAD_RIGHT_BOUNDARY:
#         player_car.x += 5       # Move car right, but not past the right road boundary
    
#     # Speed control (up/down)
#     if keys[pygame.K_UP]:
#         player_speed = min(player_speed + ACCELERATION, MAX_SPEED)  # Accelerate upward
#     elif keys[pygame.K_DOWN]:
#         player_speed = max(player_speed - DECELERATION, MIN_SPEED)  # Decelerate or move downward
#     else:
#         # Gradually slow down to 0 if no key is pressed
#         if player_speed > 0:
#             player_speed = max(player_speed - DECELERATION, 0)
#         elif player_speed < 0:
#             player_speed = min(player_speed + DECELERATION, 0)
    
#     # Update player car position based on speed
#     player_car.y -= player_speed  # Move up if speed is positive, down if negative
    
#     # Set vertical boundaries for the player car
#     if player_car.y < 0:  # Top boundary
#         player_car.y = 0
#         player_speed = 0  # Stop upward movement
#     if player_car.y > HEIGHT - player_car.height:  # Bottom boundary
#         player_car.y = HEIGHT - player_car.height
#         player_speed = 0  # Stop downward movement
    
#     # Adjust road scrolling speed based on player speed
#     road_speed = BASE_ROAD_SPEED + player_speed  # Road scrolls faster when player accelerates
#     if road_speed < MIN_ROAD_SPEED:  # Allow slight reverse scrolling when braking
#         road_speed = MIN_ROAD_SPEED
    
#     # Scroll the road
#     road_y += road_speed
#     if road_y >= HEIGHT:
#         road_y = 0  # Reset road to bottom when it reaches top
#     elif road_y <= -HEIGHT:
#         road_y = 0  # Reset road to top if it scrolls too far backward
    
#     # Spawn traffic
#     traffic_counter += 1
#     if traffic_counter >= TRAFFIC_SPAWN_RATE:
#         traffic_counter = 0
#         # Choose a lane, avoiding the last lane used
#         available_lanes = [lane for lane in LANE_CENTERS if lane != last_lane]
#         if not available_lanes:  # If all lanes are the same as last_lane (unlikely), reset
#             available_lanes = LANE_CENTERS
#         lane_choice = random.choice(available_lanes)
#         last_lane = lane_choice  # Update last lane used
        
#         # Randomly pick a traffic car image
#         traffic_car_img = random.choice(traffic_car_images)
#         traffic_car = pygame.Rect(lane_choice, -80, 50, 80)
#         traffic.append((traffic_car, traffic_car_img))  # Store car and its image
    
#     # Move and remove traffic
#     for t in traffic[:]:  # Copy list to avoid modification issues
#         car, img = t
#         car.y += road_speed  # Move traffic with road speed
#         if car.y > HEIGHT:
#             traffic.remove(t)
#         # Check collision with player car
#         if player_car.colliderect(car):
#             print("Crash! Game Over.")
#             running = False
    
#     # Draw everything
#     screen.fill(BLACK)  # Clear screen with black background
    
#     # Draw road using tiled image
#     screen.blit(road_tile_img, (0, road_y))  # Draw upper road segment
#     if road_y > 0:
#         screen.blit(road_tile_img, (0, road_y - HEIGHT))  # Draw lower segment for seamless scrolling
#     elif road_y < 0:
#         screen.blit(road_tile_img, (0, road_y + HEIGHT))  # Draw upper segment for reverse scrolling
    
#     # Draw traffic cars using sprites
#     for car, img in traffic:
#         screen.blit(img, (car.x, car.y))  # Draw traffic car sprite
    
#     # Draw player car using sprite
#     screen.blit(player_car_img, (player_car.x, player_car.y))  # Draw at car’s position
    
#     # Update display
#     pygame.display.flip()
#     clock.tick(60)  # 60 FPS

# # Cleanup
# pygame.quit()# game.py
# Purpose: 2D car game with scrolling road (image-based), styled player car (sprite), and traffic

import pygame               # Pygame for game development
import random               # Random for traffic spawning
from face_tracker import get_face_controls, cleanup  # Import face tracking

# Initialize Pygame
pygame.init()

# Set up the game window
WIDTH = 800                 # Screen width
HEIGHT = 900                # Screen height
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Face-Controlled Car Game")
clock = pygame.time.Clock() # Control game speed

# Colors
BLACK = (0, 0, 0)           # Background
WHITE = (255, 255, 255)     # Text color

# Load and scale image assets
player_car_img = pygame.image.load("player_car.png").convert_alpha()  # Load player car sprite
player_car_img = pygame.transform.scale(player_car_img, (50, 80))     # Scale to 50x80 pixels
road_tile_img = pygame.image.load("road_v.png").convert_alpha()       # Load road tile image (already 800x600)

# Load traffic car images (2.png through 6.png)
traffic_car_images = []
for i in range(2, 7):  # From 2 to 6
    img = pygame.image.load(f"{i}.png").convert_alpha()  # Load each traffic car sprite
    img = pygame.transform.scale(img, (50, 80))          # Scale to 50x80 pixels
    traffic_car_images.append(img)

# Player car properties (using Rect for collision detection)
player_car = pygame.Rect(WIDTH // 2 - 25, HEIGHT - 100, 50, 80)  # Positioned near bottom
player_speed = 0            # Player's vertical speed (positive = up, negative = down)
MAX_SPEED = 10              # Maximum speed (upward)
MIN_SPEED = -5              # Minimum speed (downward)
ACCELERATION = 0.5          # How much speed increases per frame when accelerating
DECELERATION = 0.3          # How much speed decreases per frame when decelerating

# Road properties
road_y = 0                  # Starting position of road tile
BASE_ROAD_SPEED = 5         # Base speed of road scrolling
MIN_ROAD_SPEED = -2         # Minimum road speed (allow slight reverse when braking)
road_speed = BASE_ROAD_SPEED  # Actual road speed, influenced by player speed

# Traffic properties
traffic = []
TRAFFIC_SPAWN_RATE = 50     # Frames between spawns
traffic_counter = 0
last_lane = None            # Track the last lane used to avoid consecutive spawns

# Define lane centers for four lanes (based on 800px width, 50px car width)
LANE_CENTERS = [200, 310, 460, 580]  # Centers of four lanes

# Define road boundaries for player car (to stay off footpaths)
ROAD_LEFT_BOUNDARY = 130    # Left edge of the road (after footpath)
ROAD_RIGHT_BOUNDARY = 600   # Right edge of the road (before footpath, adjusted for car width)

# Set up font for displaying text
font = pygame.font.Font(None, 36)  # Default font, size 36

# Initialize face tracking
face_controls_gen = get_face_controls()
face_controls = next(face_controls_gen)  # Get initial control state

# Game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Get face controls
    try:
        face_controls = next(face_controls_gen)
    except StopIteration:
        print("Face tracking stopped.")
        break
    
    # Extract face control states
    tilt = face_controls["tilt"]
    eyes_closed = face_controls["eyes_closed"]
    forward_tilt = face_controls["forward_tilt"]
    
    # Horizontal movement based on head tilt (reversed: left tilt moves car right, right tilt moves car left)
    movement_text = "Not Moving"
    if tilt == "left" and player_car.x < ROAD_RIGHT_BOUNDARY:
        player_car.x += 5  # Move car right when head tilts left
        movement_text = "Moving Right"
    if tilt == "right" and player_car.x > ROAD_LEFT_BOUNDARY:
        player_car.x -= 5  # Move car left when head tilts right
        movement_text = "Moving Left"
    
    # Speed control based on forward tilt and eye state
    speed_text = "Normal Speed"
    if eyes_closed:
        # Pause the game: stop road, traffic, and player movement
        road_speed = 0
        player_speed = 0  # Stop player movement
    else:
        # Resume normal game speed
        if forward_tilt:
            player_speed = min(player_speed + ACCELERATION, MAX_SPEED)  # Accelerate when head tilted forward
            speed_text = "Speeding Up"
        else:
            # Gradually slow down to 0 if no forward tilt
            if player_speed > 0:
                player_speed = max(player_speed - DECELERATION, 0)
            elif player_speed < 0:
                player_speed = min(player_speed + DECELERATION, 0)
        
        # Adjust road scrolling speed based on player speed
        road_speed = BASE_ROAD_SPEED + player_speed
        if road_speed < MIN_ROAD_SPEED:
            road_speed = MIN_ROAD_SPEED
    
    # Update player car position based on speed (only if game is not paused)
    if not eyes_closed:
        player_car.y -= player_speed  # Move up if speed is positive, down if negative
    
    # Set vertical boundaries for the player car
    if player_car.y < 0:  # Top boundary
        player_car.y = 0
        player_speed = 0  # Stop upward movement
    if player_car.y > HEIGHT - player_car.height:  # Bottom boundary
        player_car.y = HEIGHT - player_car.height
        player_speed = 0  # Stop downward movement
    
    # Scroll the road
    road_y += road_speed
    if road_y >= HEIGHT:
        road_y = 0  # Reset road to bottom when it reaches top
    elif road_y <= -HEIGHT:
        road_y = 0  # Reset road to top if it scrolls too far backward
    
    # Spawn traffic (only if game is not paused)
    if not eyes_closed:
        traffic_counter += 1
        if traffic_counter >= TRAFFIC_SPAWN_RATE:
            traffic_counter = 0
            # Choose a lane, avoiding the last lane used
            available_lanes = [lane for lane in LANE_CENTERS if lane != last_lane]
            if not available_lanes:  # If all lanes are the same as last_lane (unlikely), reset
                available_lanes = LANE_CENTERS
            lane_choice = random.choice(available_lanes)
            last_lane = lane_choice  # Update last lane used
            
            # Randomly pick a traffic car image
            traffic_car_img = random.choice(traffic_car_images)
            traffic_car = pygame.Rect(lane_choice, -80, 50, 80)
            traffic.append((traffic_car, traffic_car_img))  # Store car and its image
    
    # Move and remove traffic (only if game is not paused)
    for t in traffic[:]:  # Copy list to avoid modification issues
        car, img = t
        if not eyes_closed:
            car.y += road_speed  # Move traffic with road speed
        if car.y > HEIGHT:
            traffic.remove(t)
        # Check collision with player car
        if player_car.colliderect(car):
            print("Crash! Game Over.")
            running = False
    
    # Draw everything
    screen.fill(BLACK)  # Clear screen with black background
    
    # Draw road using tiled image
    screen.blit(road_tile_img, (0, road_y))  # Draw upper road segment
    if road_y > 0:
        screen.blit(road_tile_img, (0, road_y - HEIGHT))  # Draw lower segment for seamless scrolling
    elif road_y < 0:
        screen.blit(road_tile_img, (0, road_y + HEIGHT))  # Draw upper segment for reverse scrolling
    
    # Draw traffic cars using sprites
    for car, img in traffic:
        screen.blit(img, (car.x, car.y))  # Draw traffic car sprite
    
    # Draw player car using sprite
    screen.blit(player_car_img, (player_car.x, player_car.y))  # Draw at car’s position
    
    # Draw status text
    movement_surface = font.render(movement_text, True, WHITE)
    screen.blit(movement_surface, (10, 10))  # Top-left corner
    
    speed_surface = font.render(speed_text, True, WHITE)
    screen.blit(speed_surface, (10, 50))  # Below movement text
    
    pause_surface = font.render("Game Paused: Eyes Closed" if eyes_closed else "Game Running", True, WHITE)
    screen.blit(pause_surface, (10, 90))  # Below speed text
    
    # Update display
    pygame.display.flip()
    clock.tick(60)  # 60 FPS

# Cleanup
pygame.quit()
cleanup(cv2.VideoCapture(0))  # Release webcam resources