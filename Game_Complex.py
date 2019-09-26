import pygame
import random 
from sys import exit

pygame.init()

# set variables for width and height to maintain consistency 
WIDTH = 800
HEIGHT = 600 

#speed
SPEED = 10

# colour red, blue and yellow 
RED = (255,0,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)

#player size
player_size = 50

# position of player within the screen
player_pos = [WIDTH/2, HEIGHT-2* player_size]

#Background colour
Background_Colour = (0,0,0)

enemy_size = 50

# random position of enemy 
enemy_pos = [random.randint(0, WIDTH - enemy_size),0]
enemy_list = [enemy_pos]

# launches the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# initial condition to be false
game_over = False

score = 0 

# clock is a function used for FPS of the game 
clock = pygame.time.Clock()

myFont = pygame.font.SysFont("monospace", 35)


def set_level(score, SPEED):
	if score < 20:
		SPEED = 10
	elif score < 40:
		SPEED = 14
	elif score < 60:
		SPEED = 18
	else:
		SPEED = 20

	return SPEED


def drop_enemies(enemy_list): # this function is used to drop enemy rectangles randomly
	delay = random.random()
	if len(enemy_list) < 10 and delay < 0.1:
		x_pos = random.randint(0, WIDTH - enemy_size)
		y_pos = 0
		enemy_list.append([x_pos, y_pos])


def draw_enemies(enemy_list): # this function is used to create more enemies 
	for enemy_pos in enemy_list:
		pygame.draw.rect(screen, BLUE, (enemy_pos [0], enemy_pos [1], enemy_size, enemy_size))


def update_enemy_positions(enemy_list, score): # update enemy positions and reset 
	for idx, enemy_pos in enumerate(enemy_list):
		if enemy_pos[1] >= 0 and enemy_pos[1] < HEIGHT:
			enemy_pos[1] += SPEED
		else:
			enemy_list.pop(idx)
			score += 1 # adds score once the enemy falls off 

	return score

def collision_check(enemy_list, bplayer_pos): # this checks if a collision has occured 
	for enemy_pos in enemy_list:
		if detect_collision(enemy_pos, player_pos):
			return True
	return False

def detect_collision(player_pos, enemy_pos):  
	p_x = player_pos[0]
	p_y = player_pos[1]

	e_x = enemy_pos[0]
	e_y = enemy_pos[1]

	# to detect any collisions around the edges of rectangle using x and y co-ordinates
	if (e_x >= p_x and e_x < (p_x + player_size)) or (p_x >= e_x and p_x < (e_x + enemy_size)):
		if (e_y >= p_y and e_y < (p_y + player_size)) or (p_y >= e_y and p_y < (e_y + enemy_size)):
			return True 
	return False

# movement of player position when clicking on left and right arrow keys
while not game_over:	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()

		if event.type == pygame.KEYDOWN:
			x = player_pos [0]
			y = player_pos [1]

			if event.key == pygame.K_LEFT:
				x -= player_size

			elif event.key == pygame.K_RIGHT:
				x += player_size

			player_pos = [x,y]

	screen.fill(Background_Colour)

	
	drop_enemies(enemy_list)
	score = update_enemy_positions(enemy_list, score)
	SPEED = set_level(score, SPEED)

	text = "Score:" + str(score)
	label = myFont.render(text, 1, YELLOW)
	screen.blit(label, (WIDTH-200, HEIGHT-40))

	# checking if collision occured and to stop if it did 
	if collision_check(enemy_list,player_pos):
		game_over = True
		

	draw_enemies(enemy_list)

	# create a rectangle for player 
	pygame.draw.rect(screen, RED, (player_pos [0], player_pos [1], player_size, player_size))

	clock.tick(30)

	pygame.display.update()