import pygame, sys, random, asyncio, time
from game import Game


SCREEN_WIDTH = 750
SCREEN_HEIGHT = 700
OFFSET = 50
GREY = (29, 29, 28)
YELLOW = (243, 216, 63)

#Pygame settings
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH + OFFSET, SCREEN_HEIGHT + 2 * OFFSET))
pygame.display.set_caption("Space Invaders")
clock = pygame.time.Clock()
game = Game(SCREEN_WIDTH, SCREEN_HEIGHT, OFFSET)

#UI
font = pygame.font.Font("Fonts/monogram.ttf", 40)
level_surface = font.render("LEVEL 01", False, YELLOW)
game_over_surface = font.render("GAME OVER", False, YELLOW)
score_text_surface = font.render("SCORE", False, YELLOW)
highscore_text_surface = font.render("HIGH-SCORE", False, YELLOW)

#Custom events
SHOOT_LASER = pygame.USEREVENT #for Alien's lasers
pygame.time.set_timer(SHOOT_LASER, 300)
SPAWN_MYSTERY_SHIP = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_MYSTERY_SHIP, random.randint(8000, 14000), True)



async def main():
	while True:
		#Event handling
		event_list = pygame.event.get()
		keys = pygame.key.get_pressed()
		for event in event_list:
		    if event.type == pygame.QUIT:
		    	pygame.quit()
		    	sys.exit()
		    elif event.type == SHOOT_LASER and game.run:
		    	game.alien_shoot_laser()
		    elif event.type == SPAWN_MYSTERY_SHIP and game.run:
		    	game.create_mystery_ship()
		    	#pygame.time.set_timer(SPAWN_MYSTERY_SHIP, random.randint(8000, 14000), True)
		    elif keys[pygame.K_SPACE] and game.run == False:
		    	game.reset()
		    else:
		    	continue


		#Updating
		if game.run:
			game.spaceship_group.update()
			game.move_aliens_sideways() #includes downward movements
			game.aliens_lasers_group.update()
			game.mysteryship_group.update()
			game.check_for_collisions()

		#Drawing UI
		screen.fill(GREY)
		pygame.draw.rect(screen, YELLOW, (10, 10, 780, 780), 2, 0, 60, 60, 60, 60)
		pygame.draw.line(screen, YELLOW, (25, 730), (775, 730), 3)

		if game.run:
			screen.blit(level_surface, (570, 740, 50, 50))
		else:
			screen.blit(game_over_surface, (570, 740, 50, 50))

		for life in range(game.lives):
			screen.blit(game.spaceship_group.sprite.image, (50 * (1 + life), 745))

		screen.blit(score_text_surface, (50, 15, 50, 50))
		formatted_score = str(game.score).zfill(5)
		score_surface = font.render(formatted_score, False, YELLOW)
		screen.blit(score_surface, (50, 40, 50, 50))

		screen.blit(highscore_text_surface, (550, 15, 50, 50))
		formatted_highscore = str(game.highscore).zfill(5)
		highscore_surface = font.render(formatted_highscore, False, YELLOW)
		screen.blit(highscore_surface, (625, 40, 50, 50))

		#Drawing Objects
		game.spaceship_group.draw(screen)
		game.spaceship_group.sprite.lasers_group.draw(screen) #game.spaceship.lasers_group.draw(screen) works the same
		for obstacle in game.obstacles:
			obstacle.blocks_group.draw(screen)
		game.aliens_group.draw(screen)
		game.aliens_lasers_group.draw(screen)
		game.mysteryship_group.draw(screen)

		pygame.display.flip()
		clock.tick(60)  # limits FPS to 60
		await asyncio.sleep(0)

asyncio.run(main())
