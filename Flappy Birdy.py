import pygame, sys, random

def draw_floor():
	screen.blit(floor_serface, (floor_x_pos, 620))
	screen.blit(floor_serface, (floor_x_pos + 403, 620))

def create_pipe():
	random_pipe_pos = random.choice(pipr_height)
	bottom_pipe = pipe_surface.get_rect(midtop = (500, random_pipe_pos))
	top_pipe = pipe_surface.get_rect(midtop = (500, random_pipe_pos - 640))
	return top_pipe, bottom_pipe

def move_pipe(pipes):
	for pipe in pipes:
		pipe.centerx -=5
	visible_pipes = [pipe for pipe in pipes if pipe.right > -50]
	return pipes

def draw_pipes(pipes):
	for pipe in pipes:
		if pipe.bottom >= 716:
			screen.blit(pipe_surface, pipe)
		else:
			flip_pipe = pygame.transform.flip(pipe_surface, False, True)
			screen.blit(flip_pipe, pipe)

def check_col(pipes):
	global can_score
	for pipe in pipes:
		if bird_rect.colliderect(pipe):
			death_sound.play()
			can_score = True
			return False

	if bird_rect.top <= -150 or bird_rect.bottom >= 620:
		can_score = True
		death_sound.play()
		return False

	return True

def rotate_bird(bird):
	new_bird = pygame.transform.rotozoom(bird, bird_move * -3, 1)
	return new_bird

def bird_animation():
	new_bird = bird_frames[bird_index]
	new_bird_rect = new_bird.get_rect(center = (70, bird_rect.centery))
	return new_bird, new_bird_rect

def score_display(game_state):
	if game_state == "main_game":
		score_surf = game_font.render(str(int(score)), True, (255, 255,255))
		score_rect = score_surf.get_rect(center = (201, 100))
		screen.blit(score_surf, score_rect)
	if game_state == 'game_over':
		score_surf = game_font.render(f'Score: {int(score)}', True, (255, 255,255))
		score_rect = score_surf.get_rect(center = (201, 100))
		screen.blit(score_surf, score_rect)

		high_score_surf = game_font.render(f'High Score: {int(high_score)}', True, (255, 255,255))
		high_score_rect = high_score_surf.get_rect(center = (201, 580))
		screen.blit(high_score_surf, high_score_rect)

def update_score(score, high_score):
	if score > high_score:
		high_score = score
	return high_score

def pipe_score_check():
	global score, can_score

	if pipe_list:
		for pipe in pipe_list:
			if 65 < pipe.centerx < 75 and can_score:
				score += 1
				score_sound.play()
				can_score = False
			if pipe.centerx < 0:
				can_score = True


pygame.init()
screen = pygame.display.set_mode((403, 716))
clock = pygame.time.Clock()
game_font = pygame.font.Font('04B_19.ttf' ,40)

#Game physics
gravity = 0.25
bird_move = 0
game_active = True
score = 0
high_score = 0
can_score = True

back_ground = pygame.image.load('assets/background-day.png').convert()
back_ground = pygame.transform.scale(back_ground, (403, 716))

floor_serface = pygame.image.load('assets/base.png').convert()
floor_serface = pygame.transform.scale(floor_serface, (470, 156))
floor_x_pos = 0

bird_downflap = pygame.image.load('assets/bluebird-downflap.png').convert_alpha()
bird_downflap = pygame.transform.scale(bird_downflap, (48, 34))
bird_midflap = pygame.image.load('assets/bluebird-downflap.png').convert_alpha()
bird_midflap = pygame.transform.scale(bird_midflap, (48, 34))
bird_upflap = pygame.image.load('assets/bluebird-upflap.png').convert_alpha()
bird_upflap = pygame.transform.scale(bird_upflap, (48, 34))
bird_frames = [bird_downflap, bird_midflap, bird_upflap]
bird_index = 0
bird_surf = bird_frames[bird_index]
bird_rect = bird_surf.get_rect(center = (70, 358))

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)

#bird_surf = pygame.image.load('assets/bluebird-midflap.png').convert_alpha()
#bird_surf = pygame.transform.scale(bird_surf, (48, 34))
#bird_rect = bird_surf.get_rect(center = (70, 358))

pipe_surface = pygame.image.load('assets/pipe-green.png')
pipe_surface = pygame.transform.scale(pipe_surface, (72, 420))
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)
pipr_height = [330, 400, 500, 570]

game_over_surface = pygame.image.load('assets/message.png').convert_alpha()
game_over_surface = pygame.transform.scale(game_over_surface, (257, 374))
game_over_rect = game_over_surface.get_rect(center = (201, 358))

flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')
death_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
score_sound = pygame.mixer.Sound('sound/sfx_point.wav')



while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type ==pygame.KEYDOWN:
			if event.key == pygame.K_SPACE and game_active == True:
				bird_move = 0
				bird_move -= 9
				flap_sound.play()
			if event.key == pygame.K_SPACE and game_active == False:
				game_active = True
				pipe_list.clear()
				bird_rect.center = (70, 358)
				bird_move = 0
				score = 0

		if event.type ==SPAWNPIPE:
			pipe_list.extend(create_pipe())

		if event.type == BIRDFLAP:
			if bird_index < 2:
				bird_index += 1
			else:
				bird_index = 0

			bird_surf, bird_rect = bird_animation()

	screen.blit(back_ground,(0, 0))
	if game_active:
		#bird
		bird_move += gravity
		rotated_bird = rotate_bird(bird_surf)
		bird_rect.centery += bird_move
		screen.blit(rotated_bird, bird_rect)
		game_active = check_col(pipe_list)

		#pipes
		pipe_list = move_pipe(pipe_list)
		draw_pipes(pipe_list)

		pipe_score_check()
		score_display('main_game')
	else:
		screen.blit(game_over_surface, game_over_rect)
		high_score = update_score(score, high_score)
		score_display('game_over')


	#floor
	floor_x_pos -= 1
	draw_floor()
	if floor_x_pos <= -403:
		floor_x_pos = 0


	pygame.display.update()
	clock.tick(60)
