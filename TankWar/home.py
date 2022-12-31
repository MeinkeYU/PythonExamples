# coding: utf-8
# Home Class
import pygame


# Home class
class Home(pygame.sprite.Sprite):  # Size of image of home is 48 * 48.
	def __init__(self): # Initialization
		pygame.sprite.Sprite.__init__(self)
		self.homes = ['./images/home/home1.png', './images/home/home2.png', './images/home/home_destroyed.png']
		self.home = pygame.image.load(self.homes[0])
		self.rect = self.home.get_rect()
		# Home has a fixed location at the bottom.
		self.rect.left, self.rect.top = (3 + 12 * 24, 3 + 24 * 24)
		self.alive = True

	# Home set to destroy.
	def set_dead(self):
        # After the home is destroyed, show the image of the path contained in the last element of the list named homes.
		self.home = pygame.image.load(self.homes[-1])
		self.alive = False
