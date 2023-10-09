import pygame

class Laser(pygame.sprite.Sprite):
	def __init__(self, position, speed, screen_height, offset):
		super().__init__()
		self.image = pygame.Surface((4,15))
		self.image.fill((243, 216, 63))
		self.rect = self.image.get_rect(center = position)
		self.speed = speed
		self.screen_height = screen_height
		self.offset = offset

	def update(self):
		self.rect.y -= self.speed
		#17 is the Where the line starts minus its line thickness
		if self.rect.top > self.screen_height + 17 or self.rect.bottom < self.offset/2:
			self.kill()

