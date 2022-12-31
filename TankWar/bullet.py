# coding: utf-8
# Bullet Class
import pygame


# Bullet class
class Bullet(pygame.sprite.Sprite):  # Image size of bullet is 12 * 12
	def __init__(self): # Initialization
		pygame.sprite.Sprite.__init__(self)
		# Four directions of bullet (up and down, left and right)
		self.bullets = ['./images/bullet/bullet_up.png', './images/bullet/bullet_down.png', './images/bullet/bullet_left.png', './images/bullet/bullet_right.png']
		# Bullet direction (default value is up)
		self.direction_x, self.direction_y = 0, -1
		self.bullet = pygame.image.load(self.bullets[0]) # Load the image of the bullet facing upwards.
		self.rect = self.bullet.get_rect()# image.get_rect() get the position of the image and return a rect object to be stored in the rect variable.
		# Assign actual values in the tank class again
		self.rect.left, self.rect.right = 0, 0
		# Speed
		self.speed = 6
		# Survival or not
		self.being = False
		# Whether it is a strengthened version of the bullet (can destroy iron)
		self.stronger = False

	# Change bullet direction
	def turn(self, direction_x, direction_y):
		self.direction_x, self.direction_y = direction_x, direction_y
		# Depending on the orientation, different bullet appearances are loaded
		if self.direction_x == 0 and self.direction_y == -1:    # UP
			self.bullet = pygame.image.load(self.bullets[0])
		elif self.direction_x == 0 and self.direction_y == 1:   # DOWN
			self.bullet = pygame.image.load(self.bullets[1])
		elif self.direction_x == -1 and self.direction_y == 0:  # LEFT
			self.bullet = pygame.image.load(self.bullets[2])
		elif self.direction_x == 1 and self.direction_y == 0:   # RIGHT
			self.bullet = pygame.image.load(self.bullets[3])
		else:
			raise ValueError('Bullet class -> direction value error.') # Exception error report

	# Move
	def move(self):
		# pygame.rect.move(arg1,arg2) is used to move the object on the screen with rect, arg1,arg2 are the offsets.
		self.rect = self.rect.move(self.speed*self.direction_x, self.speed*self.direction_y) 
		# Disappear after reaching the edge of the map.
		# The window size is 630*630. 3 pixels are reserved around it.
		if (self.rect.top < 3) or (self.rect.bottom > 630 - 3) or (self.rect.left < 3) or (self.rect.right > 630 - 3): 
			self.being = False # The tank can only fire again when the bullets disappear, so the being value should be set to False.
