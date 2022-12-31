# coding: utf-8
# Food Class
import pygame
import random


# Food class, used to enhance tank capabilities.
class Food(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		# The path of the corresponding food image is assigned to the variable.
		# Destroy all current enemies.
		self.food_bomb = './images/food/food_bomb.png'
		# All current enemies are stationary for a period of time.
		self.food_clock = './images/food/food_clock.png'
		# Make tank bullets can break iron.
		self.food_gun = './images/food/food_gun.png'
		# Turn the wall of the base camp into a iron one.
		#self.food_iron = './images/food/food_gun.png'    # BUG
		self.food_iron = './images/food/food_iron.png'
		# The tank gains a protect mask for a period of time.
		self.food_protect = './images/food/food_protect.png'
		# Tank upgrades.
		self.food_star = './images/food/food_star.png'
		# Life of tank plus 1.
		self.food_tank = './images/food/food_tank.png'
		# All foods, creating a list called foods.
		self.foods = [self.food_bomb, self.food_clock, self.food_gun, self.food_iron, self.food_protect, self.food_star, self.food_tank]
		# Temporarily set to None, to generate a random type of food when generate() is called.
		# Initialize food-related property variables.
		self.kind = None
		self.food = None
		self.rect = None
		# Whether exist or not
		self.being = False
		# Time of existence
		self.time = 1000

	# Generate food
	def generate(self):
		self.kind = random.randint(0, 6) # Randomly take values from 0 to 6 and assign kind numbers to variable kind.
		self.food = pygame.image.load(self.foods[self.kind]).convert_alpha()
		self.rect = self.food.get_rect()
		# Randomly take values for left and top in the range of 100 to 500
  		# Randomly generate coordinates for food (randomly appear in the map)
		self.rect.left, self.rect.top = random.randint(100, 500), random.randint(100, 500) 
		self.being = True
