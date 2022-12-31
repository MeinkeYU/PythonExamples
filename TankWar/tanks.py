# coding: utf-8
# Tank Class
import pygame
import random
from bullet import Bullet


# myTank class
class myTank(pygame.sprite.Sprite): # 48 * 48
	MAX_DIR_CHANGE_CACHE_CNT = 5
	def __init__(self, player): # The first argument of the init method is always "self", which represents the created instance itself.
		pygame.sprite.Sprite.__init__(self)
		# Player Number (1/2)
		self.player = player
		# Different players with different tanks (different levels correspond to different images).
		# The list stores the image paths, three images correspond to three levels.
  		# Each image contains two groups of four different orientations of the same tank.
		if player == 1:
			self.tanks = ['./images/myTank/tank_T1_0.png', './images/myTank/tank_T1_1.png', './images/myTank/tank_T1_2.png']
		elif player == 2:
			self.tanks = ['./images/myTank/tank_T2_0.png', './images/myTank/tank_T2_1.png', './images/myTank/tank_T2_2.png']
		else:
			raise ValueError('myTank class -> player value error.') # Customizable exception handling
		# Tank level (Initial value is 0)
		self.level = 0
  
		# Load 
		# Two tank images are for wheel effects, because the two tank images of the wheel tracks are different.
        # Display two images alternately, it will have the effect that the track is rotating.
        
        # convert_alpha, as opposed to convert, retains the Alpha channel information of the image, which can be considered as retaining the transparent part.
		self.tank = pygame.image.load(self.tanks[self.level]).convert_alpha() 
		self.tank_0 = self.tank.subsurface((0, 0), (48, 48)) # Take out each sub-image of the image with the subsurface().
		self.tank_1 = self.tank.subsurface((48, 0), (48, 48)) # subsurface((left, top), (width, height))
		# image.get_rect(): get the position of the image
		# Return a rect object to be stored in the rect variable, which encapsulates the shape and position of any object in the game.
		self.rect = self.tank_0.get_rect() 
		# Protect mask,  image size is 96*48.
		self.protected_mask = pygame.image.load('./images/others/protect.png').convert_alpha()
		self.protected_mask1 = self.protected_mask.subsurface((0, 0), (48, 48)) 
		self.protected_mask2 = self.protected_mask.subsurface((48, 0), (48, 48))
		# Tank direction, the default value is up.
		self.direction_x, self.direction_y = 0, -1
		# Different players have different birth locations.
		if player == 1:
			self.rect.left, self.rect.top = 3 + 24 * 8, 3 + 24 * 24 # self.rect: where is the sprite image displayed
		elif player == 2:
			self.rect.left, self.rect.top = 3 + 24 * 16, 3 + 24 * 24
		else:
			raise ValueError('myTank class -> player value error.')
		# Tank speed
		self.speed = 3
		# Survival or not
		self.being = True
		# Life value
		self.life = 3
		# If you set this variable to True, you can enter cheat mode and keep our tank in protect mask.
		self.protected = True
		# bullet 
        # Instantiation of Bullet class
		self.bullet = Bullet()

	# Shoot
	def shoot(self):
		# Cannot fire again until the previous bullet is disappeared.
		self.bullet.being = True
		stronger = self.bullet.stronger
		# According to the current direction and position of the tank, set the direction and position of the bullet.
        # The bullet appears not far in front of the tank.
		self.bullet.turn(self.direction_x, self.direction_y)   # Call the turn() in Bullet class to change the bullet orientation and image.
		if self.direction_x == 0 and self.direction_y == -1:   # UP
			self.bullet.rect.left = self.rect.left + 20
			self.bullet.rect.bottom = self.rect.top - 1
		elif self.direction_x == 0 and self.direction_y == 1:  # DOWN
			self.bullet.rect.left = self.rect.left + 20
			self.bullet.rect.top = self.rect.bottom + 1
		elif self.direction_x == -1 and self.direction_y == 0:  # LEFT
			self.bullet.rect.right = self.rect.left - 1
			self.bullet.rect.top = self.rect.top + 20
		elif self.direction_x == 1 and self.direction_y == 0:   # RIGHT
			self.bullet.rect.left = self.rect.right + 1
			self.bullet.rect.top = self.rect.top + 20
		else:
			raise ValueError('myTank class -> direction value error.')
		# The speed of bullets will be accelerated when the tank's level is increased.
        # After level 2 and above, it can destroy the iron.
		# Change the variable values of bullet speed and stronger according to tank level.
		if self.level == 0:
			self.bullet.speed = 8
			self.bullet.stronger = False
		elif self.level == 1:
			self.bullet.speed = 12
			self.bullet.stronger = False
		elif self.level == 2:
			self.bullet.speed = 12
			self.bullet.stronger = True
		elif self.level == 3:     # BUG, Images are only available for Level 0 to Level 2, no images of Level 3 tanks
			self.bullet.speed = 16
			self.bullet.stronger = True
		else:
			raise ValueError('myTank class -> level value error.')
		# added, 2021.01.16
		# When the stronger is True, update the stronger value of the object bullet instantiated by the Bullet class from False to True.
		if stronger:
			self.bullet.stronger = stronger

	# Level up
	def up_level(self):
		#if self.level < 3:    # Bug
		if self.level < 2:
			self.level += 1
		try:
			self.tank = pygame.image.load(self.tanks[self.level]).convert_alpha()
		except:
			# If the try statement throws an exception, the last element (image path) in the tanks list is loaded
			self.tank = pygame.image.load(self.tanks[-1]).convert_alpha() 

	# Level down
	def down_level(self):
		if self.level > 0:
			self.level -= 1
		self.tank = pygame.image.load(self.tanks[self.level]).convert_alpha()

	# Try to move along the direction of the tank
	def try_move(self):
		# rect.move(), move the rect object. This requires a pair of parameters [x,y]
  		# One for the velocity of the move in the x direction and one for the velocity of the move in the y direction. 
    	# This is used to specify the offset address of the new object.
		self.rect = self.rect.move(self.speed * self.direction_x, self.speed * self.direction_y)

	# Undo move (achieved by reversing the move)
	def undo_move(self):
		self.rect = self.rect.move(self.speed * -self.direction_x, self.speed * -self.direction_y)

	def detect_and_undo(self, tankGroup, brickGroup, ironGroup, myhome):
		# Is it movable
		is_move = True
		# Determine if tank is outside the four boundaries of the map, and if it collides with brick walls, iron walls, other tanks and home.
		"""
        Rectangle conflict detection between sprites and groups: see if the rectangle regions intersect, 
        by comparing each Sprite's Sprite.rect property to determine the intersection.
        
        pygame.sprite.spritecollide(sprite, sprite_group, bool, collided = None))。
        When this function is called, all sprites in a group are checked for conflicts one by one against another single sprite, 
        and the conflicting sprites are returned as a list.
        
        The first argument of this function is a single sprite, the second argument is a group of sprites, and the third argument is a bool value. 
        When True, all conflicting sprites in the group will be deleted, when False, no conflicting sprites will be deleted.
        
        The collided parameter is the callback function used to calculate collisions, if no collisions are passed, 
        all sprites must have the value of rect, which is the rectangle of the sprite area that will be used to calculate collisions.
		"""
		# Can't move when the tank beyond the map boundary, conflicts with bricks, iron, other tanks and home.
		if self.rect.top < 3 or self.rect.bottom > 630 - 3 or \
				self.rect.left < 3 or self.rect.right > 630 - 3 or \
				pygame.sprite.spritecollide(self, brickGroup, False, None) or \
				pygame.sprite.spritecollide(self, ironGroup, False, None) or  \
				pygame.sprite.spritecollide(self, tankGroup, False, None) or \
				pygame.sprite.collide_rect(self, myhome): 
                # pygame.sprite.collide_rect(): rectangle detection between two sprites, 
                # whether the rectangular areas intersect. Returns True for a collision, False otherwise.
			self.undo_move()
			is_move = False
		return is_move

	def do_move(self, tankGroup, brickGroup, ironGroup, myhome, dx, dy, x0y0, w0h0, x1y1, w1h1):
		# Change orientation
		self.direction_x, self.direction_y = dx, dy
		# Resetting the appearance of the tank according to the orientation
		self.tank_0 = self.tank.subsurface(x0y0, w0h0)
		self.tank_1 = self.tank.subsurface(x1y1, w1h1)
		# Move first, determine later
		self.try_move()
		return self.detect_and_undo(tankGroup, brickGroup, ironGroup, myhome) # If there is a conflict, call undo_move() to undo the move


	# Move up
	def move_up(self, tankGroup, brickGroup, ironGroup, myhome):
		return self.do_move(tankGroup, brickGroup, ironGroup, myhome,
							0, -1,
							(0, 0), (48, 48),
							(48, 0), (48, 48)) # Tank faces up, call do_move(), use subsurface to take out the first row of tank images

	# Move down
	def move_down(self, tankGroup, brickGroup, ironGroup, myhome):
		return self.do_move(tankGroup, brickGroup, ironGroup, myhome,
							0, 1,
							(0, 48), (48, 48),
							(48, 48), (48, 48)) # Tank faces up, call do_move(), use subsurface to take out the second row of tank images

	# Move left
	def move_left(self, tankGroup, brickGroup, ironGroup, myhome):
		return self.do_move(tankGroup, brickGroup, ironGroup, myhome,
							-1, 0,
							(0, 96), (48, 48),
							(48, 96), (48, 48)) # Tank faces up, call do_move(), use subsurface to take out the third row of tank images

	# Move right
	def move_right(self, tankGroup, brickGroup, ironGroup, myhome):
		return self.do_move(tankGroup, brickGroup, ironGroup, myhome,
							1, 0,
							(0, 144), (48, 48),
							(48, 144), (48, 48)) # Tank faces right, call do_move(), use subsurface to take out the fourth row of tank images

	# Reset after death, when our tank is dead.
	def reset(self):
		# Reset tank level.
		self.level = 0
		# Reset protect mask effect.
		self.protected = False
		# Reset the appearance of the tank.
		self.tank = pygame.image.load(self.tanks[self.level]).convert_alpha()
		# Tank orientation is up by default.
		self.tank_0 = self.tank.subsurface((0, 0), (48, 48))
		self.tank_1 = self.tank.subsurface((48, 0), (48, 48))
		self.rect = self.tank_0.get_rect()
		self.direction_x, self.direction_y = 0, -1
		# Give different players different initial positions.
		if self.player == 1:
			self.rect.left, self.rect.top = 3 + 24 * 8, 3 + 24 * 24
		elif self.player == 2:
			self.rect.left, self.rect.top = 3 + 24 * 16, 3 + 24 * 24
		else:
			raise ValueError('myTank class -> player value error.')
		self.speed = 3
		# Reset shell strength.
		self.bullet.stronger = False


# enemyTank class
class enemyTank(pygame.sprite.Sprite):
    # Default value parameter. When instantiating, the number of real parameters may not be equal to the number of formal parameters.
	def __init__(self, x=None, kind=None, is_red=None): 
		pygame.sprite.Sprite.__init__(self)
		# Used to play birth effects for a newly generated tank.
		self.born = True
		# The birth effect time is 90 ticks. Determine the real time needed based on tick().
  		# If tick(60), the interface is refreshed 60 times per second, the birth effect takes about 1.5 seconds.
		self.times = 90
		# Type of enemy tank number: from 0 to 3
		if kind is None:
			self.kind = random.randint(0, 3)
		else:
			self.kind = kind
		# All enemy tanks: there are 4 types of kind. The same kind, internally also divided into 4 different colors.
		# Each list element is a different color tank.
		self.tanks1 = ['./images/enemyTank/enemy_1_0.png', './images/enemyTank/enemy_1_1.png', './images/enemyTank/enemy_1_2.png', './images/enemyTank/enemy_1_3.png']
		self.tanks2 = ['./images/enemyTank/enemy_2_0.png', './images/enemyTank/enemy_2_1.png', './images/enemyTank/enemy_2_2.png', './images/enemyTank/enemy_2_3.png']
		self.tanks3 = ['./images/enemyTank/enemy_3_0.png', './images/enemyTank/enemy_3_1.png', './images/enemyTank/enemy_3_2.png', './images/enemyTank/enemy_3_3.png']
		self.tanks4 = ['./images/enemyTank/enemy_4_0.png', './images/enemyTank/enemy_4_1.png', './images/enemyTank/enemy_4_2.png', './images/enemyTank/enemy_4_3.png']
		# Each list element is a different kind of tank
		self.tanks = [self.tanks1, self.tanks2, self.tanks3, self.tanks4]
		# Whether to carry food (red tanks carry food) 
		if is_red is None:
			self.is_red = random.choice((True, False, False, False, False)) # 0.2 probability of the tank being red.
		else:
			self.is_red = is_red
		# added
		# self.is_red = True
		# Tanks of the same type have different colors, red tanks have a little more blood than their counterparts.
		if self.is_red:
			self.color = 3 # The element numbered 3 in the list is the red tank image
		else:
			self.color = random.randint(0, 2)
		# Blood amount according to color
		self.blood = self.color 
		# self.tank corresponding to the image (96*192), containing the 8 images of appearance of tanks (48*48)
		self.tank = pygame.image.load(self.tanks[self.kind][self.color]).convert_alpha()
		# Two tank images are for wheel effects
		self.tank_0 = self.tank.subsurface((0, 48), (48, 48))
		self.tank_1 = self.tank.subsurface((48, 48), (48, 48))
		self.rect = self.tank_0.get_rect()
		# Tank positions: left, center and right positions on the top. Enemy tanks appear randomly in the three positions.
		if x is None:
			self.x = random.randint(0, 2)
		else:
			self.x = x
		self.rect.left, self.rect.top = 3 + self.x * 12 * 24, 3
		# Whether the tank can move or not
		self.can_move = True
		# Tank speed
		self.speed = max(3 - self.kind, 1)
		# direction
		self.direction_x, self.direction_y = 0, 1
		# Survival or not
		self.being = True
		# bullet
		self.bullet = Bullet()
  
	# Shoot
	def shoot(self):
		self.bullet.being = True
		self.bullet.turn(self.direction_x, self.direction_y)
		if self.direction_x == 0 and self.direction_y == -1:     # UP
			self.bullet.rect.left = self.rect.left + 20
			self.bullet.rect.bottom = self.rect.top - 1
		elif self.direction_x == 0 and self.direction_y == 1:    # DOWN
			self.bullet.rect.left = self.rect.left + 20
			self.bullet.rect.top = self.rect.bottom + 1
		elif self.direction_x == -1 and self.direction_y == 0:   # LEFT
			self.bullet.rect.right = self.rect.left - 1
			self.bullet.rect.top = self.rect.top + 20
		elif self.direction_x == 1 and self.direction_y == 0:    # RIGHT
			self.bullet.rect.left = self.rect.right + 1
			self.bullet.rect.top = self.rect.top + 20
		else:
			raise ValueError('enemyTank class -> direction value error.')

	# Try to move along the direction of the tank
	def try_move(self):
        # pygame.rect.move(arg1,arg2): used to move rect objects on the screen, arg1,arg2 are the offsets
		self.rect = self.rect.move(self.speed * self.direction_x, self.speed * self.direction_y)

	# Undo move (achieved by reversing the move)
	def undo_move(self):
		self.rect = self.rect.move(self.speed * -self.direction_x, self.speed * -self.direction_y)

	# Generate random directions
	def random_direction(self):
		self.direction_x, self.direction_y = random.choice(([0, 1], [0, -1], [1, 0], [-1, 0]))

	# Random movement (enemy tank)
	def move(self, tankGroup, brickGroup, ironGroup, myhome):
		# 1% probability of randomly changing the direction of movement
		if random.randint(0, 99) == 0:
			self.random_direction()
		# According to the current orientation of the tank, set its appearance. 
 		# self.tank corresponds to the image (96*192), which contains 8 images of the appearance of tank(48*48)
		if self.direction_x == 0 and self.direction_y == -1:        # UP
			self.tank_0 = self.tank.subsurface((0, 0), (48, 48))    # ((left, top), (width, height))
			self.tank_1 = self.tank.subsurface((48, 0), (48, 48))
		elif self.direction_x == 0 and self.direction_y == 1:       # DOWN
			self.tank_0 = self.tank.subsurface((0, 48), (48, 48))
			self.tank_1 = self.tank.subsurface((48, 48), (48, 48))
		elif self.direction_x == -1 and self.direction_y == 0:      # LEFT
			self.tank_0 = self.tank.subsurface((0, 96), (48, 48))
			self.tank_1 = self.tank.subsurface((48, 96), (48, 48))
		elif self.direction_x == 1 and self.direction_y == 0:       # RIGHT
			self.tank_0 = self.tank.subsurface((0, 144), (48, 48))
			self.tank_1 = self.tank.subsurface((48, 144), (48, 48))
		else:
			raise ValueError('enemyTank class -> direction value error.')
		# Move first, determine later
		self.try_move()
		is_move = True
		# Determine if tank is outside the four boundaries of the map, and if it collides with brick walls, iron walls, other tanks and home.
		'''
		spritecollide(sprite, group, dokill, collided = Noone)
		If the value of dokill is True, the sprites that collided in the specified sprite group will be automatically removed.
		The collided parameter is the callback function used to calculate collisions, if not specified, each sprite must have a rect attribute.
		The return value is the list of sprites in the sprite group that collided with the sprite.
  		'''
		if self.rect.top < 3 or self.rect.bottom > 630 - 3 or \
				self.rect.left < 3 or self.rect.right > 630 - 3 or \
				pygame.sprite.spritecollide(self, brickGroup, False, None) or \
				pygame.sprite.spritecollide(self, ironGroup, False, None) or  \
				pygame.sprite.spritecollide(self, tankGroup, False, None) or \
				pygame.sprite.collide_rect(self, myhome):
			# Undo the move just tried to make
			self.undo_move()
			# Randomly generate new directions of movement
			self.random_direction()
			is_move = False
		return is_move

	# Reload the image of the tank appearance, because after the enemy tank is hit, the amount of blood will be reduced and the color will be changed.
	def reload(self):
		self.tank = pygame.image.load(self.tanks[self.kind][self.color]).convert_alpha()
		self.tank_0 = self.tank.subsurface((0, 48), (48, 48))
		self.tank_1 = self.tank.subsurface((48, 48), (48, 48))
