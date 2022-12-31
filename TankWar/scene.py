# coding: utf-8
# Scene Class (brick, river, tree, ice, iron)
import pygame
import random


# Brick wall
class Brick(pygame.sprite.Sprite):  # Image size is 24 * 24
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.brick = pygame.image.load('./images/scene/brick.png') 
		"""  
        get_rect() returns a rect object to be stored in the rect variable, which encapsulates the shape and position of any object in the game. 
        It is easy for the caller to use.
        The rect object is a rectangular area that is actually drawn. 
        
        The properties obtained from the rect object are the following:
		x,y
		top, left, bottom, right
		topleft, bottomleft, topright, bottomright
		midtop, midleft, midbottom, midright
		center, centerx, centery
		size, width, height
		w,h
		"""
		self.rect = self.brick.get_rect() # image.get.rect() to get the location of rect object.
		self.being = False # Whether the scene elements exist or not


# Iron wall
class Iron(pygame.sprite.Sprite):   #  Image size is 24 * 24
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.iron = pygame.image.load('./images/scene/iron.png')
		self.rect = self.iron.get_rect()
		self.being = False # Whether the scene elements exist or not


# Ice
class Ice(pygame.sprite.Sprite):  #  Image size is 12 * 12
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.ice = pygame.image.load('./images/scene/ice.png')
		self.rect = self.ice.get_rect()
		self.being = False # Whether the scene elements exist or not


# River
class River(pygame.sprite.Sprite):  #  Image size is 12 * 12
	def __init__(self, kind=None):
		pygame.sprite.Sprite.__init__(self)
		if kind is None:
			self.kind = random.randint(0, 1)
		self.rivers = ['./images/scene/river1.png', './images/scene/river2.png']
		self.river = pygame.image.load(self.rivers[self.kind])
		self.rect = self.river.get_rect()
		self.being = False # Whether the scene elements exist or not


# Tree
class Tree(pygame.sprite.Sprite):    # Image size is 12 * 12
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.tree = pygame.image.load('./images/scene/tree.png')
		self.rect = self.tree.get_rect()
		self.being = False # Whether the scene elements exist or not

# Map
class Map():
	def __init__(self, stage):
		# Create sprite groups for each scene element, for managing a large number of sprites (scene element images)
		self.brickGroup = pygame.sprite.Group()
		self.ironGroup = pygame.sprite.Group()
		self.iceGroup = pygame.sprite.Group()
		self.riverGroup = pygame.sprite.Group()
		self.treeGroup = pygame.sprite.Group()
		# commented
				# commented
		# if stage == 1:
		# 	self.stage1()
		# elif stage == 2:
		# 	self.stage2()
		# Calling the set stage method
		self.set_stage(stage) # This method is called automatically whenever the Map class is instantiated in the initialization function.
	
	def set_stage(self, stage=1): # Default value parameter, can be called without parameter
		# Call the corresponding stage method based on the stage number 
		if stage == 1:
			self.stage1()
		elif stage == 2:
			self.stage2()
		elif stage == 3:
			self.stage3()
		elif stage == 4:
			self.stage4()
		elif stage == 5:
			self.stage5()
		elif stage == 6:
			self.stage6()
  
    #Q1 
	def stageQ1(self):
		# Set the position coordinate values of the scene element images into a list
		for x, y in [(1, 8), (2, 7), (3, 6), (4, 5), (5, 4), (6, 3), (7, 2), (8, 1), (9, 2), (10, 3), (11, 4), 
               (12, 5), (13, 6), (14, 7), (15, 8), (6, 7), (7, 7), (8, 7), (9, 7), (10, 7), (3, 10), (4, 10), (5, 10), 
               (6, 10), (7, 10), (8, 10), (9, 10), (10, 10), (11, 10), (12, 10), (13, 10), (8, 8), (8, 9), (8, 11), 
               (8, 12), (8, 13), (8, 14), (8, 15), (8, 16), (7, 16), (6, 15), (3, 14), (4, 13), (5, 12), (11, 12), (12, 13), (13, 14), 
               (11, 23), (12, 23), (13, 23), (14, 23), (11, 24), (14, 24), (11, 25), (14, 25)]:
				brick = Brick() # Instantiate the scene element class to be displayed.
				brick.rect.left, brick.rect.top = 3 + x * 24, 3 + y * 24 # The brick scene element image size is 24*24, with 3 pixels reserved around the map.
				brick.being = True # Scene elements exist
				self.brickGroup.add(brick) # By looping, each scene element sprite is added to the sprite group
    
    #Q2 
	def stageQ2(self):
		for x, y in [(1, 8), (2, 7), (3, 6), (4, 5), (5, 4), (6, 3), (7, 2), (8, 1), (9, 2), (10, 3), (11, 4), 
               (12, 5), (13, 6), (14, 7), (15, 8), (6, 7), (7, 7), (8, 7), (9, 7), (10, 7), (3, 10), (4, 10), (5, 10), 
               (6, 10), (7, 10), (8, 10), (9, 10), (10, 10), (11, 10), (12, 10), (13, 10), (8, 8), (8, 9), (8, 11), 
               (8, 12), (8, 13), (8, 14), (8, 15), (8, 16), (7, 16), (6, 15), (3, 14), (4, 13), (5, 12), (11, 12), (12, 13), (13, 14)]:
				brick = Brick()
				brick.rect.left, brick.rect.top = 3 + x * 24, 3 + y * 24
				brick.being = True
				self.brickGroup.add(brick)
		# Cheat mode: the home is always protected by iron wall
		self.protect_home() # Calling can add iron wall around the home
	
	#Q3 
	def stageQ3(self):
		for x, y in [(1, 8), (2, 7), (3, 6), (4, 5), (5, 4), (6, 3), (7, 2), (8, 1), (9, 2), (10, 3), (11, 4), 
               (12, 5), (13, 6), (14, 7), (15, 8), (6, 7), (7, 7), (8, 7), (9, 7), (10, 7), (3, 10), (4, 10), (5, 10), 
               (6, 10), (7, 10), (8, 10), (9, 10), (10, 10), (11, 10), (12, 10), (13, 10), (8, 8), (8, 9), (8, 11), 
               (8, 12), (8, 13), (8, 14), (8, 15), (8, 16), (7, 16), (6, 15), (3, 14), (4, 13), (5, 12), (11, 12), (12, 13), (13, 14)]:
				brick = Brick()
				brick.rect.left, brick.rect.top = 3 + x * 24, 3 + y * 24
				brick.being = True
				self.brickGroup.add(brick)
				# The x of the tree is 1/2 of the brick, the original is to translate 16 squares of 24*24 to reach the position.
    			# Now the squares become 12*12. So the number of moves should be doubled
				x += 16*2 
				tree = Tree() 
				tree.rect.left, tree.rect.top = 3 + x * 12, 3 + y * 12 # The tree scene element image size is 12*12, with 3 pixels reserved around the map
				tree.being = True
				self.treeGroup.add(tree)
		self.protect_home()
  
	# Stage 1 "澳"
	def stage1(self):  # 630 * 630;    630 = 24 * 26 + 6 = 24 * 26 + 3 * 2
		for x, y in [(9, 1), (3, 2), (8, 2), (4, 3), (6, 3), (7, 3), (8, 3), (9, 3), (10, 3), (11, 3), (12, 3), (13, 3), (14, 3),
               (4, 4), (6, 4), (14, 4), (1, 5), (6, 5), (8, 5), (10, 5), (12, 5), (14, 5), (2, 6), (6, 6), (10, 6), (14, 6), (2, 7),
               (6, 7), (7, 7), (8, 7), (9, 7), (10, 7), (11, 7), (12, 7), (13, 7), (14, 7), (4, 8), (6, 8), (9, 8), (10, 8), (11, 8),
               (14, 8), (4, 9), (6, 9), (8, 9), (10, 9), (12, 9), (14, 9), (3, 10), (6, 10), (14, 10), (1, 11), (2, 11), (3, 11), 
               (10, 11), (3, 12), (5, 12), (6, 12), (7, 12), (8, 12), (9, 12), (10, 12), (11, 12), (12, 12), (13, 12), (14, 12), (15, 12),
               (3, 13), (9, 13), (11, 13), (3, 14), (8, 14), (12, 14), (3, 15), (7, 15), (13, 15), (5, 16), (6, 16), (14, 16), (15, 16)]:
				brick = Brick()
				brick.rect.left, brick.rect.top = 3 + x * 24, 3 + y * 24
				brick.being = True
				self.brickGroup.add(brick)
				# The x of the tree is 1/2 of the brick, the original is to translate 16 squares of 24*24 to reach the position.
    			# Now the squares become 12*12. So the number of moves should be doubled
				x += 16*2 
				tree = Tree()
				tree.rect.left, tree.rect.top = 3 + x * 12, 3 + y * 12 # The tree scene element image size is 12*12, with 3 pixels reserved around the map
				tree.being = True
				self.treeGroup.add(tree)
		self.protect_home()
  
	# Stage 2 "门"
	def stage2(self):
		for x, y in [(3, 4), (3, 5), (3, 6), (3, 7), (3, 8), (3, 9), (3, 10), (3, 11), (3, 12), (3, 13), (3, 14), (3, 15), (3, 16),
               (4, 1), (5, 2), (5, 3), (8, 2), (9, 2), (10, 2), (11, 2), (12, 2), (13, 2), (14, 2), (15, 2), (15, 3), (15, 4), (15, 5), (15, 6), (15, 7),
               (15, 8), (15, 9), (15, 10), (15, 11), (15, 12), (15, 13), (15, 14), (15, 15), (14, 16)]:
				brick = Brick()
				brick.rect.left, brick.rect.top = 3 + x * 24, 3 + y * 24
				brick.being = True
				self.brickGroup.add(brick)
				# The x of the tree is 1/2 of the brick, the original is to translate 16 squares of 24*24 to reach the position.
    			# Now the squares become 12*12. So the number of moves should be doubled
				x += 16*2
				tree = Tree()
				tree.rect.left, tree.rect.top = 3 + x * 12, 3 + y * 12 # The tree scene element image size is 12*12, with 3 pixels reserved around the map
				tree.being = True
				self.treeGroup.add(tree)
		self.protect_home()
 
	# Stage 3 "科"
	def stage3(self):
		for x, y in [(1, 3), (1, 6), (1, 12), (2, 3), (2, 6), (2, 10), (2, 11), (3, 3), (3, 6), (3, 8), (3, 9), (4, 2), (4, 3),
               (4, 4), (4, 5), (4, 6), (4, 7), (4, 8), (4, 9), (4, 10), (4, 11), (4, 12), (4, 13), (4, 14), (4, 15), (4, 16), (5, 1), (5, 2), (5, 6),
               (5, 8), (6, 2), (6, 6), (6, 9), (8, 2), (8, 6), (8, 11), (9, 3), (9, 4), (9, 7), (9, 8), (9, 11), (10, 11), (11, 11), (12, 1),
               (12, 2), (12, 3), (12, 4), (12, 5), (12, 6), (12, 7), (12, 8), (12, 9), (12, 10), (12, 11), (12, 12), (12, 13), (12, 14), (12, 15),
               (12, 16), (13, 10), (14, 10), (15, 10)]:
				brick = Brick()
				brick.rect.left, brick.rect.top = 3 + x * 24, 3 + y * 24
				brick.being = True
				self.brickGroup.add(brick)
				# The x of the tree is 1/2 of the brick, the original is to translate 16 squares of 24*24 to reach the position.
    			# Now the squares become 12*12. So the number of moves should be doubled
				x += 16*2 
				tree = Tree()
				tree.rect.left, tree.rect.top = 3 + x * 12, 3 + y * 12 # The tree scene element image size is 12*12, with 3 pixels reserved around the map
				tree.being = True
				self.treeGroup.add(tree)
		self.protect_home() 
  
	# Stage 4 "技"
	def stage4(self):
		for x, y in [(1, 5), (1, 11), (2, 5), (2, 11), (2, 15), (3, 5), (3, 10), (3, 16), (4, 1), (4, 2), (4, 3), (4, 4), (4, 5),
               (4, 6), (4, 7), (4, 8), (4, 9), (4, 10), (4, 11), (4, 12), (4, 13), (4, 14), (4, 15), (5, 5), (5, 9), (6, 5), (6, 8),
               (6, 16), (7, 4), (7, 16), (8, 4), (8, 8), (8, 15), (9, 4), (9, 8), (9, 9), (9, 10), (9, 15), (10, 4), (10, 8), (10, 11), (10, 12),
               (10, 14), (11, 1), (11, 2), (11, 3), (11, 4), (11, 5), (11, 6), (11, 7), (11, 8), (11, 13), (12, 4), (12, 8), (12, 12), (12, 14),
               (13, 4), (13, 8), (13, 10), (13, 11), (13, 15), (14, 4), (14, 8), (14, 9), (14, 16), (15, 4), (15, 16)]:
				brick = Brick()
				brick.rect.left, brick.rect.top = 3 + x * 24, 3 + y * 24
				brick.being = True
				self.brickGroup.add(brick)
				# The x of the tree is 1/2 of the brick, the original is to translate 16 squares of 24*24 to reach the position.
    			# Now the squares become 12*12. So the number of moves should be doubled
				x += 16*2 
				tree = Tree()
				tree.rect.left, tree.rect.top = 3 + x * 12, 3 + y * 12 # The tree scene element image size is 12*12, with 3 pixels reserved around the map
				tree.being = True
				self.treeGroup.add(tree)
		self.protect_home() 

	# Stage 5 "大"
	def stage5(self):
		for x, y in [(1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6), (8, 6), (9, 6), (10, 6), (11, 6), (12, 6), (13, 6),
               (14, 6), (15, 6), (8, 1), (8, 2), (8, 3), (8, 4), (8, 5), (8, 7), (8, 8), (7, 9), (7, 10), (6, 11), (6, 12), (5, 13), (4, 14), (3, 15),
               (1, 16), (2, 16), (9, 9), (9, 10), (10, 11), (10, 12), (11, 13), (12, 14), (13, 15), (14, 16), (15, 16)]:
				brick = Brick()
				brick.rect.left, brick.rect.top = 3 + x * 24, 3 + y * 24
				brick.being = True
				self.brickGroup.add(brick)
				# The x of the tree is 1/2 of the brick, the original is to translate 16 squares of 24*24 to reach the position.
    			# Now the squares become 12*12. So the number of moves should be doubled
				x += 16*2
				tree = Tree()
				tree.rect.left, tree.rect.top = 3 + x * 12, 3 + y * 12 # The tree scene element image size is 12*12, with 3 pixels reserved around the map
				tree.being = True
				self.treeGroup.add(tree)
		self.protect_home() 
 
 	# Stage 6 "学"
	def stage6(self):
		for x, y in [(3, 1), (4, 2), (4, 3), (7, 1), (8, 2), (8, 3), (13, 1), (13, 2), (12, 3), (11, 4), (1, 7), (2, 5), (2, 6),
               (3, 5), (4, 5), (5, 5), (6, 5), (7, 5), (8, 5), (9, 5), (10, 5), (11, 5), (12, 5), (13, 5), (14, 5), (15, 5), (15, 6), (15, 7), (4, 8),
               (5, 8), (6, 8), (7, 8), (8, 8), (9, 8), (10, 8), (11, 8), (10, 9), (8, 10), (9, 10), (1, 11), (2, 11), (3, 11), (4, 11), (5, 11), (6, 11),
               (7, 11), (8,11), (9, 11), (10, 11), (11, 11), (12, 11), (13, 11), (14, 11), (15, 11), (8, 12), (8, 13), (8, 14), (8, 15), (7, 16),
               (6, 15)]:
				brick = Brick()
				brick.rect.left, brick.rect.top = 3 + x * 24, 3 + y * 24
				brick.being = True
				self.brickGroup.add(brick)
				# The x of the tree is 1/2 of the brick, the original is to translate 16 squares of 24*24 to reach the position.
    			# Now the squares become 12*12. So the number of moves should be doubled
				x += 16*2
				tree = Tree()
				tree.rect.left, tree.rect.top = 3 + x * 12, 3 + y * 12 # The tree scene element image size is 12*12, with 3 pixels reserved around the map
				tree.being = True
				self.treeGroup.add(tree)
		self.protect_home() 
  
    # Protect home
	def protect_home(self):
		for x, y in [(11, 23), (12, 23), (13, 23), (14, 23), (11, 24), (14, 24), (11, 25), (14, 25)]:
			iron = Iron() # use iron
			iron.rect.left, iron.rect.top = 3 + x * 24, 3 + y * 24
			iron.being = True
			self.ironGroup.add(iron)
