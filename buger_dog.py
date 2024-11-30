import pygame
import random

# Initialize pygame
pygame.init()

# Set a display surface
WIDTH = 800
HEIGHT = 600
display_surface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Burger Dog')

# Set FPS and clock
FPS = 60
clock = pygame.time.Clock()

# Set game value
PLAYER_STARTING_LIVES = 3
PLAYER_NORMAL_VELOCITY = 5
PLAYER_BOOST_VELOCITY = 10
STARTING_BOOST_LEVEL = 100
STARTING_BURGER_VELOCITY = 3
BURGER_ACCELERATION = .25
BUFFER_DISTANCE = 100

score = 0
burger_points = 0
burgers_eaten = 0

player_lives = PLAYER_STARTING_LIVES
player_velocity = PLAYER_NORMAL_VELOCITY
boost_level = STARTING_BOOST_LEVEL

burger_velocity = STARTING_BURGER_VELOCITY

# Set colors
ORANGE = (246, 170, 54)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Set fonts
font = pygame.font.Font('assets/WashYourHand.ttf', 32)
font2 = pygame.font.Font('assets/WashYourHand.ttf', 18)

# Set text
points_text = font.render('Burger Points: ' + str(burger_points), True, ORANGE)
points_text_rect = points_text.get_rect()
points_text_rect.topleft = (10, 10)

score_text = font.render('Score: ' + str(score), True, ORANGE)
score_text_rect = score_text.get_rect()
score_text_rect.topleft = (10, 50)

title_text = font.render('>>Burger Dog<<', True, WHITE)
title_text_rect = title_text.get_rect()
title_text_rect.centerx = WIDTH // 2
title_text_rect.y = 10

eaten_text = font.render('Burgers Eaten: ' + str(burgers_eaten), True, ORANGE)
eaten_text_rect = eaten_text.get_rect()
eaten_text_rect.centerx = WIDTH // 2
eaten_text_rect.y = 50

lives_text = font.render('Lives: ' + str(player_lives), True, ORANGE)
lives_text_rect = lives_text.get_rect()
lives_text_rect.topright = (WIDTH - 10, 10)

boost_text = font.render('Boost: ' + str(boost_level), True, ORANGE)
boost_text_rect = boost_text.get_rect()
boost_text_rect.topright = (WIDTH - 10, 50)

game_over_text = font.render('FINAL SCORE: ' + str(score), True, ORANGE)
game_over_text_rect = score_text.get_rect()
game_over_text_rect.center = (WIDTH // 2 - 70, HEIGHT // 2 - 50)

continue_text = font.render('Press ENTER to play again', True, WHITE)
continue_text_rect = score_text.get_rect()
continue_text_rect.centerx = WIDTH // 2 - 130
continue_text_rect.centery = HEIGHT // 2 + 32

created_by_text = font2.render('Created by: MAHYAR', True, WHITE)
created_by_text_rect = created_by_text.get_rect()
created_by_text_rect.bottomright = (WIDTH - 10, HEIGHT - 10)

paused_text = font.render('PAUSED', True, WHITE, BLACK)
paused_text_rect = paused_text.get_rect()
paused_text_rect.center = (WIDTH // 2, HEIGHT // 2)

# Set sounds and music
bark_sound = pygame.mixer.Sound('assets/bark_sound.wav')
bark_sound.set_volume(.05)
miss_sound = pygame.mixer.Sound('assets/miss_sound.wav')
miss_sound.set_volume(.05)
pygame.mixer.music.load('assets/bd_background_music.wav')
pygame.mixer.music.set_volume(.05)

# Set images
# Dog image
player_image_right = pygame.image.load('assets/dog_right.png')
player_image_left = pygame.image.load('assets/dog_left.png')
player_image = player_image_left

player_image_rect = player_image_left.get_rect()
player_image_rect.centerx = WIDTH // 2
player_image_rect.bottom = HEIGHT

# Burger image
burger_image = pygame.image.load('assets/burger.png')
burger_image_rect = burger_image.get_rect()
burger_image_rect.topleft = (random.randint(0, WIDTH - 32), -BUFFER_DISTANCE)

# Hide the mouse
pygame.mouse.set_visible(False)

# Paused game state
paused = False

# Main game loop
pygame.mixer.music.play()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                paused = not paused
                display_surface.blit(paused_text, paused_text_rect)

    if not paused:
        # Move the player
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_image_rect.left > 0:
            player_image_rect.x -= player_velocity
            player_image = player_image_left
        if keys[pygame.K_RIGHT] and player_image_rect.right < WIDTH:
            player_image_rect.x += player_velocity
            player_image = player_image_right
        if keys[pygame.K_UP] and player_image_rect.top > 103:
            player_image_rect.y -= player_velocity
        if keys[pygame.K_DOWN] and player_image_rect.bottom < HEIGHT:
            player_image_rect.y += player_velocity

        # Engage boost
        if keys[pygame.K_SPACE] and boost_level > 0:
            player_velocity = PLAYER_BOOST_VELOCITY
            boost_level -= 1
        else:
            player_velocity = PLAYER_NORMAL_VELOCITY

        # Move the burger and update burger points
        burger_image_rect.y += burger_velocity
        burger_points = int(burger_velocity * (HEIGHT - burger_image_rect.y + 100))

        # Player missed the burger
        if burger_image_rect.y > HEIGHT:
            player_lives -= 1
            miss_sound.play()

            burger_image_rect.topleft = (random.randint(0, WIDTH - 32), -BUFFER_DISTANCE)
            burger_velocity = STARTING_BURGER_VELOCITY

            player_image_rect.centerx = WIDTH // 2
            player_image_rect.bottom = HEIGHT
            boost_level = STARTING_BOOST_LEVEL

        # Check for collisions
        if player_image_rect.colliderect(burger_image_rect):
            score += burger_points
            burgers_eaten += 1
            bark_sound.play()

            burger_image_rect.topleft = (random.randint(0, WIDTH - 32), -BUFFER_DISTANCE)
            burger_velocity += BURGER_ACCELERATION

            boost_level += 25
            if boost_level > STARTING_BOOST_LEVEL:
                boost_level = STARTING_BOOST_LEVEL

        # Update the HUD
        points_text = font.render('Burger Points: ' + str(burger_points), True, ORANGE)
        boost_text = font.render('Boost: ' + str(boost_level), True, ORANGE)
        lives_text = font.render('Lives: ' + str(player_lives), True, ORANGE)
        eaten_text = font.render('Burgers Eaten: ' + str(burgers_eaten), True, ORANGE)
        score_text = font.render('Score: ' + str(score), True, ORANGE)

        # Check for game over
        if player_lives == 0:
            display_surface.fill(BLACK)

            player_image_rect.center = (WIDTH // 2, HEIGHT // 2 - 120)
            game_over_text = font.render('FINAL SCORE: ' + str(score), True, ORANGE)

            display_surface.blit(player_image, player_image_rect)
            display_surface.blit(game_over_text, game_over_text_rect)
            display_surface.blit(continue_text, continue_text_rect)

            pygame.display.update()

            # Pause the game
            pygame.mixer.music.stop()
            is_paused = True
            while is_paused:
                for event in pygame.event.get():
                    # Player wants to continue
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            player_image_rect.bottom = HEIGHT
                            score = 0
                            burgers_eaten = 0
                            player_lives = PLAYER_STARTING_LIVES
                            boost_level = STARTING_BOOST_LEVEL
                            burger_velocity = STARTING_BURGER_VELOCITY

                            pygame.mixer.music.play()
                            is_paused = False

                    if event.type == pygame.QUIT:
                        is_paused = False
                        running = False

        # Fill the surface
        display_surface.fill(BLACK)

        # Blit the HUD
        display_surface.blit(points_text, points_text_rect)
        display_surface.blit(score_text, score_text_rect)
        display_surface.blit(title_text, title_text_rect)
        display_surface.blit(eaten_text, eaten_text_rect)
        display_surface.blit(lives_text, lives_text_rect)
        display_surface.blit(boost_text, boost_text_rect)
        display_surface.blit(created_by_text, created_by_text_rect)
        pygame.draw.line(display_surface, WHITE, (0, 100), (WIDTH, 100), 3)

        # Blit assets
        display_surface.blit(player_image, player_image_rect)
        display_surface.blit(burger_image, burger_image_rect)

    # Update the screen and clock
    pygame.display.flip()
    clock.tick(FPS)

# End game
pygame.quit()