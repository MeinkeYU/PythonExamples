# coding: utf-8
# The main game running program
import sys
import pygame
import scene
import bullet
import food
import tanks
import home
from pygame.locals import *

# Global variables (function-wide effect)
is_gameover = False
NUM_OF_STAGES = 6
"""
The whole game screen is cleared and the whole map is redrawn 60 times within one second.
If the variable being of the game element is set to False (which means it is not alive), it will not be shown in the screen by calling blit().
This has the effect of removing it from the game map.
"""

# Start interface display
def show_start_interface(screen, width, height):
	"""
	Font(filename, size): load a font file from outside to draw the text
	filename, a string format, the path to the font file
	size, set the size of the font
	"""
	tfont = pygame.font.Font('./font/simkai.ttf', width//4) # exact division
	cfont = pygame.font.Font('./font/simkai.ttf', width//20)
	"""
    render(text, antialias, color, background=None)
	Function: draw text on the new Surface
    text: the text content to be drawn
	antialias: boolean parameter, whether it is a smooth font (anti-aliasing)
	color: set the font color
	background: optional parameter, default is None, this parameter is used to set the background color of the font
	"""
	title = tfont.render(u'坦克大战', True, (255, 0, 0))
	content1 = cfont.render(u'按1键进入单人游戏', True, (0, 0, 255))
	content2 = cfont.render(u'按2键进入双人人游戏', True, (0, 0, 255))
	trect = title.get_rect()
    # midtop: The center (x, y) of the length of the top of the rectangle of rect
	trect.midtop = (width/2, height/4)
	crect1 = content1.get_rect()
	crect1.midtop = (width/2, height/1.8)
	crect2 = content2.get_rect()
	crect2.midtop = (width/2, height/1.6)
    # The surface.blit(image, rect) method is designed to draw one image to another, using the top-left coordinates (left, top) of rect.
	# Add the drawn image to the main screen.
	screen.blit(title, trect)
	screen.blit(content1, crect1)
	screen.blit(content2, crect2)
	"""
    Pygame has a display surface that can be included in the window or run full screen.
    Update allows updating only a part of the screen, not the whole area. The updated part is displayed on the screen. 
    If no parameters are passed, it will update the entire surface area.
    """
	pygame.display.update()
	while True:
		for event in pygame.event.get(): # Loop to get events, listen to event state, use get() to get events.                            
      		# Judgment the events (1. Clicking the close button 2. Pressing a key on the keyboard)
			# Tap the window's x to exit the function
			if event.type == QUIT:
				sys.exit() # Terminate the system, the program exits directly without catching an exception
			# Determine if the event type is a key press
   			# if yes: continue to determine which key is pressed and process it accordingly
			elif event.type == pygame.KEYDOWN: 
				if event.key == pygame.K_1: # Keyboard press 1, return 1 (select player 1)
					return 1
				if event.key == pygame.K_2: # Keyboard press 2, return 2 (select player 2)
					return 2


# End interface display
def show_end_interface(screen, width, height, is_win):
	bg_img = pygame.image.load("./images/others/background.png")   # 630 * 630
	# surface.blit(image, (x, y)) The image is drawn on the (x, y) coordinates of the screen
	screen.blit(bg_img, (0, 0)) # Load the background on the window first, to achieve the effect of clearing the screen
	if is_win: # Game pass
		font = pygame.font.Font('./font/simkai.ttf', width//10)
		content = font.render(u'恭喜通关！', True, (255, 0, 0))
		rect = content.get_rect()
		rect.midtop = (width/2, height/2)
		screen.blit(content, rect)
	else:
		fail_img = pygame.image.load("./images/others/gameover.png")  # 64 * 32
		rect = fail_img.get_rect()
		rect.midtop = (width/2, height/2)
		screen.blit(fail_img, rect)
	# pygame.display.update() 
    # Update part of the content to be displayed on the screen, if there is no parameter, it is the same as the flip function
	pygame.display.update() 
	while True:
		for event in pygame.event.get(): # Loop to get events, listen to event state, use get() to get events
			if event.type == QUIT:
				sys.exit()


# Stage switch interface display
def show_switch_stage(screen, width, height, stage):
	bg_img = pygame.image.load("./images/others/background.png")
	screen.blit(bg_img, (0, 0))
	font = pygame.font.Font('./font/simkai.ttf', width//10)
	content = font.render(u'第%d关' % stage, True, (0, 255, 0))
	rect = content.get_rect()
	rect.midtop = (width/2, height/2)
	screen.blit(content, rect)
	pygame.display.update()
    # To create multiple user events with pygame.USEREVENT, just add 1 to this constant
    # The fourth timer constant is set, so add 3 to USEREVENT
	delay_event = pygame.constants.USEREVENT + 3 # USEREVENT triggers a user event 
	"""
    The timer can create a user event that can be detected by the event loop within a specified time period
    pygame.time.set_timer(event, millis, loops=0): create a timer. Every once in a while, perform some action
	Set an event to appear on the event queue every given number of milliseconds. 
    The first event will not appear until the amount of time has passed.
    The event attribute can be a pygame.event.Event object or an integer type that denotes an event.
    loops is an integer that denotes the number of events posted. If 0 (default) then the events will keep getting posted, 
    unless explicitly stopped.
	"""
	# Trigger delay_event every 5000ms, call the function.
    # To achieve the stage switching interface display for 5000ms.
	pygame.time.set_timer(delay_event, 5000, loops=1) 
	while True:
		for event in pygame.event.get():
			# Determine if the user has clicked the close button
			if event.type == QUIT:
				# Exiting the system
				sys.exit()
			if event.type == delay_event:
				return # Directly jump out of the function


# Our tank
def handle_mytanksGroup(stage_data, screen):
    # Realize dynamic effect of tank tracks and protect mask effect
	if stage_data.tank_player1 in stage_data.mytanksGroup:
		# When the player presses the arrow keys, player1_moving = True. 
  		# When the tank is moving, the effect of the movement of the tank tracks is displayed by switching between two different images.
		if stage_data.is_switch_tank and stage_data.player1_moving:
			# Display one of the tank track effects to the coordinates of the current tank position.
			screen.blit(stage_data.tank_player1.tank_0, (stage_data.tank_player1.rect.left, stage_data.tank_player1.rect.top))
			stage_data.player1_moving = False # Enter the else statement, and display another image of the tank tracks.
		else:
			screen.blit(stage_data.tank_player1.tank_1, (stage_data.tank_player1.rect.left, stage_data.tank_player1.rect.top))
		# When there is a protect mask effect, protected = True。
		if stage_data.tank_player1.protected:
			# Draw protect mask picture to current tank position
			screen.blit(stage_data.tank_player1.protected_mask1, (stage_data.tank_player1.rect.left, stage_data.tank_player1.rect.top))
	if stage_data.num_player > 1: # Press 2 at the start interface, select two-player mode. 
		if stage_data.tank_player2 in stage_data.mytanksGroup:
			if stage_data.is_switch_tank and stage_data.player2_moving:
				screen.blit(stage_data.tank_player2.tank_0, (stage_data.tank_player2.rect.left, stage_data.tank_player2.rect.top))
				#player1_moving = False  # BUG
				stage_data.player2_moving = False
			else:
				screen.blit(stage_data.tank_player2.tank_1, (stage_data.tank_player2.rect.left, stage_data.tank_player2.rect.top))
			if stage_data.tank_player2.protected:
				screen.blit(stage_data.tank_player1.protected_mask1, (stage_data.tank_player2.rect.left, stage_data.tank_player2.rect.top))


# Enemy tank
def handle_enemytanksGroup(stage_data, screen):
    # Implement enemy tank birth effects and track dynamic effects.
	for each in stage_data.enemytanksGroup:
		# Birth effects
		if each.born: # Allow the display of birth effects.
			if each.times > 0:
				each.times -= 1 # Count down
				# There are 3 pictures of the star from small to large, the appearance changes every 10 ticks.
        		# Within 90 ticks, a total of 3 times from small to large effects can be displayed.
				if each.times <= 10:
					screen.blit(stage_data.appearances[2], (3 + each.x * 12 * 24, 3))
				elif each.times <= 20:
					screen.blit(stage_data.appearances[1], (3 + each.x * 12 * 24, 3))
				elif each.times <= 30:
					screen.blit(stage_data.appearances[0], (3 + each.x * 12 * 24, 3))
				elif each.times <= 40:
					screen.blit(stage_data.appearances[2], (3 + each.x * 12 * 24, 3))
				elif each.times <= 50:
					screen.blit(stage_data.appearances[1], (3 + each.x * 12 * 24, 3))
				elif each.times <= 60:
					screen.blit(stage_data.appearances[0], (3 + each.x * 12 * 24, 3))
				elif each.times <= 70:
					screen.blit(stage_data.appearances[2], (3 + each.x * 12 * 24, 3))
				elif each.times <= 80:
					screen.blit(stage_data.appearances[1], (3 + each.x * 12 * 24, 3))
				elif each.times <= 90:
					screen.blit(stage_data.appearances[0], (3 + each.x * 12 * 24, 3))
			else:
				# Birth effect ends
				each.born = False
		else:
			# Change the orientation of the enemy tank only when it is allowed to move
			if each.can_move:
				stage_data.tanksGroup.remove(each) # Remove the enemy tank sprite which has not yet moved.
				each.move(stage_data.tanksGroup, stage_data.map_stage.brickGroup,stage_data.map_stage.ironGroup, stage_data.myhome)
				stage_data.tanksGroup.add(each) # Add the moved enemy tank sprite to the sprite group.
			# Enemy tank, always show track effect, even after being stationary by food_clock, track still spinning in place.
			if stage_data.is_switch_tank:
				# Two tank track effects switch back and forth
				screen.blit(each.tank_0, (each.rect.left, each.rect.top))
				# In 5 ticks, allow is_switch_tank to flip once, then enter the else statement
			else:
				screen.blit(each.tank_1, (each.rect.left, each.rect.top))



# Our Bullets  Collision event
def handle_mybullet(stage_data, sound_data, screen):
	global is_gameover 
	# After the bullet disappears, you can shoot the next one. So for one of our tanks.
	# There is only one bullet on the map, so there is no need for management of sprite group.
	for tank_player in stage_data.mytanksGroup:
		if tank_player.bullet.being:
			# Change the position of the current tank bullet, then redraw it.
			tank_player.bullet.move()
			screen.blit(tank_player.bullet.bullet, tank_player.bullet.rect)
			# Bullets collide with enemy bullets.
			for each in stage_data.enemybulletsGroup:
				if each.being: # Enemy bullets exist
					# pygame.sprite.collide_rect(): Rectangle detection between two sprites, whether the rectangle areas intersect.
     				# Returns a Boolean value,. Returns True if there is a collision, otherwise returns False.
					if pygame.sprite.collide_rect(tank_player.bullet, each): # Collision occurred
						tank_player.bullet.being = False # Enemy bullets disappear
						each.being = False # Our bullets disappear
						stage_data.enemybulletsGroup.remove(each) # Enemy bullet sprite removed from sprite group.
						break # Loop termination
				else: # Enemy bullets do not exist directly removed.
					stage_data.enemybulletsGroup.remove(each)
			# Bullets collide with enemy tanks.
			for each in stage_data.enemytanksGroup:
				if each.being: # Enemy tank exists
					if pygame.sprite.collide_rect(tank_player.bullet, each): # Our bullets have a collision with the enemy tank.
						# When a red tank is hit, a random bonus is generated.
						if each.is_red: # The enemy tank that collided is red.
							myfood = food.Food() # Food class in food.py
							myfood.generate() # generate food
							stage_data.myfoodsGroup.add(myfood) # Generated food sprites are added to the sprite group.
							each.is_red = False # After being hit, the color changes, not red.
						# When the enemy tank is hit, the blood volume is reduced and the tank color is changed.
						each.blood -= 1
						each.color -= 1
						if each.blood < 0:
							sound_data.bang_sound.play() # Play sound effects when defeating enemy tanks.
							each.being = False
							stage_data.enemytanksGroup.remove(each) # Remove from enemy tank sprite group.
							stage_data.enemytanks_now -= 1 # The number of enemy tanks present on the field is reduced by 1.
							stage_data.tanksGroup.remove(each) # Remove from all tank sprite group.
						else:
							each.reload() # If the blood level is not 0, reload the appearance of the enemy tank in the current color.
						tank_player.bullet.being = False # Our bullets disappear.
						break # Jump out of the loop
				else: # Enemy tank does not exist, remove directly
					stage_data.enemytanksGroup.remove(each)
					stage_data.tanksGroup.remove(each)
			# Bullets collide with brick walls
			# True, then the sprites in the specified sprite group that collided will be automatically removed
			if pygame.sprite.spritecollide(tank_player.bullet, stage_data.map_stage.brickGroup, True, None):
				tank_player.bullet.being = False

			# Bullets collide with iron walls
			if tank_player.bullet.stronger: # When the bullet is stronger, it will break the iron
				if pygame.sprite.spritecollide(tank_player.bullet, stage_data.map_stage.ironGroup, True, None):
					tank_player.bullet.being = False
			else:
				if pygame.sprite.spritecollide(tank_player.bullet, stage_data.map_stage.ironGroup, False, None):
					tank_player.bullet.being = False

			# Bullets collide with home
			if pygame.sprite.collide_rect(tank_player.bullet, stage_data.myhome):
				tank_player.bullet.being = False
				stage_data.myhome.set_dead()
				is_gameover = True # home is destroyed, game is over.


# Enemy Bullets  Collision event
def handle_enemy_bullet(stage_data, sound_data, screen):
	global is_gameover
	for each in stage_data.enemytanksGroup:
		if each.being:
			# Enemy tank can move, and is not firing
			if each.can_move and not each.bullet.being: # Bullets beyond the boundary
				stage_data.enemybulletsGroup.remove(each.bullet)
				# Enemy tank fires, set its bullets' being to True
				each.shoot()
				stage_data.enemybulletsGroup.add(each.bullet) # add to sprite group
			# The enemy tank is not in a birth effect state
			if not each.born:
				if each.bullet.being:
					# The enemy bullets fly forward, update the position, and then redraw.
					each.bullet.move()
					screen.blit(each.bullet.bullet, each.bullet.rect)
					# Bullets collide with our tanks
					for tank_player in stage_data.mytanksGroup:
						if pygame.sprite.collide_rect(each.bullet, tank_player):
							# If our tank has no protect mask
							if not tank_player.protected:
								sound_data.bang_sound.play() # Play destroy sound effects
								tank_player.life -= 1 # Decrease in life value
								if tank_player.life < 0:
									stage_data.mytanksGroup.remove(tank_player)
									stage_data.tanksGroup.remove(tank_player)
									# When doubles are played, one of the two players may still be alive.
									# Only after both players are dead, the game over.
									if len(stage_data.mytanksGroup) < 1:
										is_gameover = True
								else:
									# When there are still available tanks, reset the current player's tanks.
									tank_player.reset()
							each.bullet.being = False
							stage_data.enemybulletsGroup.remove(each.bullet)
							break
					# Bullets collide with brick walls
					if pygame.sprite.spritecollide(each.bullet, stage_data.map_stage.brickGroup, True, None):
						each.bullet.being = False
						stage_data.enemybulletsGroup.remove(each.bullet)

					# Bullets collide with iron walls
					if each.bullet.stronger:
						if pygame.sprite.spritecollide(each.bullet, stage_data.map_stage.ironGroup, True, None):
							each.bullet.being = False
							# added, 2022.01.15
							stage_data.enemybulletsGroup.remove(each.bullet)
					else:
						if pygame.sprite.spritecollide(each.bullet, stage_data.map_stage.ironGroup, False, None):
							# added, 2022.01.15
							each.bullet.being = False
							stage_data.enemybulletsGroup.remove(each.bullet)

					# Bullets collide with home
					if pygame.sprite.collide_rect(each.bullet, stage_data.myhome):
						each.bullet.being = False
						stage_data.myhome.set_dead()
						is_gameover = True
		else:
			stage_data.enemytanksGroup.remove(each)
			stage_data.tanksGroup.remove(each)

# Food
def handle_food(stage_data, sound_data, screen):
	for myfood in stage_data.myfoodsGroup:
		if myfood.being and myfood.time > 0:
			screen.blit(myfood.food, myfood.rect)
			myfood.time -= 1 # Food existence time countdown
			for tank_player in stage_data.mytanksGroup:
				# When the player's tank touches food
				if pygame.sprite.collide_rect(tank_player, myfood):
					# Destroy all current enemies
					if myfood.kind == 0:
						for t in stage_data.enemytanksGroup:
							sound_data.bang_sound.play()
							# added, 2022.01.16
							stage_data.tanksGroup.remove(t)
						# Clear all tanks in the enemyTanksGroup
						stage_data.enemytanksGroup = pygame.sprite.Group() # Redefine sprite group, to clear the enemy tanks.
						# BUG. Commented 2022.01.16
						#stage_data.enemytanks_total -= stage_data.enemytanks_now
						stage_data.enemytanks_now = 0 # The number of enemy tanks on the map goes to 0.
					# Enemy stationary
					if myfood.kind == 1:
						sound_data.add_sound.play()
						for each in stage_data.enemytanksGroup:
							each.can_move = False # Enemy tanks cannot move.
						pygame.time.set_timer(stage_data.recoverEnemyEvent, 8000, loops=1) # The duration of stationary effect is 8000ms.
					# Bullet enhancement
					if myfood.kind == 2:
						sound_data.add_sound.play()
						# The original code does not work, it will be rewritten in myTank.shoot(); to modify myTank.shoot().
						tank_player.bullet.stronger = True
					# Turned the wall of home into a iron one.
					if myfood.kind == 3:
						stage_data.map_stage.protect_home()
					# The tank gains a protect mask for a period of time.
					if myfood.kind == 4:
						sound_data.add_sound.play()
						for t in stage_data.mytanksGroup:
							t.protected = True # All player tanks plus protect mask.
						pygame.time.set_timer(stage_data.noprotectMytankEvent, 8000, loops=1)  # The duration of the protect mask effect is 8000ms.
					# Tank levels up
					if myfood.kind == 5:
						sound_data.add_sound.play()
						tank_player.up_level()
					# Life value of tank plus 1
					if myfood.kind == 6:
						sound_data.add_sound.play()
						tank_player.life += 1
					myfood.being = False
					stage_data.myfoodsGroup.remove(myfood)
					break
		else:
			myfood.being = False
			stage_data.myfoodsGroup.remove(myfood)


# Handle key events related to player 1
# WSAD -> Up, Down, Left, Right
# Spacebar to shoot
def handle_player1_events(key_pressed, sound_data, stage_data):
	# As long as the user holds down the arrow keys, the tank is considered to be moving, so set player1_moving to true.
	if key_pressed[pygame.K_w]:
		stage_data.tanksGroup.remove(stage_data.tank_player1) # Remove the tank (the one before moving) sprite (image)
		stage_data.tank_player1.move_up(stage_data.tanksGroup, stage_data.map_stage.brickGroup,
											stage_data.map_stage.ironGroup, stage_data.myhome)
		stage_data.tanksGroup.add(stage_data.tank_player1) # Adding a tank (after moving) sprite (image)
		stage_data.player1_moving = True # One of the conditions for controlling track movement.
	elif key_pressed[pygame.K_s]:
		stage_data.tanksGroup.remove(stage_data.tank_player1)
		stage_data.tank_player1.move_down(stage_data.tanksGroup, stage_data.map_stage.brickGroup,
										  stage_data.map_stage.ironGroup, stage_data.myhome)
		stage_data.tanksGroup.add(stage_data.tank_player1)
		stage_data.player1_moving = True
	elif key_pressed[pygame.K_a]:
		stage_data.tanksGroup.remove(stage_data.tank_player1)
		stage_data.tank_player1.move_left(stage_data.tanksGroup, stage_data.map_stage.brickGroup,
										  stage_data.map_stage.ironGroup, stage_data.myhome)
		stage_data.tanksGroup.add(stage_data.tank_player1)
		stage_data.player1_moving = True
	elif key_pressed[pygame.K_d]:
		stage_data.tanksGroup.remove(stage_data.tank_player1)
		stage_data.tank_player1.move_right(stage_data.tanksGroup, stage_data.map_stage.brickGroup, stage_data.map_stage.ironGroup, stage_data.myhome)
		stage_data.tanksGroup.add(stage_data.tank_player1)
		stage_data.player1_moving = True
	# Modified, 2022.01.15, Allow to fire during movement
	#elif key_pressed[pygame.K_SPACE]:
	if key_pressed[pygame.K_SPACE]:
		if not stage_data.tank_player1.bullet.being: # The previous bullet disappears before you can shoot.
			sound_data.fire_sound.play()
			stage_data.tank_player1.shoot()


# Handle key events related to player 2
# ↑↓←→ -> up, down, left, right
# Keypad 0 to shoot
def handle_player2_events(key_pressed, sound_data, stage_data):
	if stage_data.num_player > 1:
		# As long as the user is holding down the arrow keys.
  		# The tank is considered to be moving, so set player2_moving to true.
		if key_pressed[pygame.K_UP]:
			stage_data.tanksGroup.remove(stage_data.tank_player2)
			stage_data.tank_player2.move_up(stage_data.tanksGroup, stage_data.map_stage.brickGroup,
												stage_data.map_stage.ironGroup, stage_data.myhome)
			stage_data.tanksGroup.add(stage_data.tank_player2)
			stage_data.player2_moving = True
		elif key_pressed[pygame.K_DOWN]:
			stage_data.tanksGroup.remove(stage_data.tank_player2)
			stage_data.tank_player2.move_down(stage_data.tanksGroup, stage_data.map_stage.brickGroup,
											  	stage_data.map_stage.ironGroup, stage_data.myhome)
			stage_data.tanksGroup.add(stage_data.tank_player2)
			stage_data.player2_moving = True
		elif key_pressed[pygame.K_LEFT]:
			stage_data.tanksGroup.remove(stage_data.tank_player2)
			stage_data.tank_player2.move_left(stage_data.tanksGroup, stage_data.map_stage.brickGroup,
											  	stage_data.map_stage.ironGroup, stage_data.myhome)
			stage_data.tanksGroup.add(stage_data.tank_player2)
			stage_data.player2_moving = True
		elif key_pressed[pygame.K_RIGHT]:
			stage_data.tanksGroup.remove(stage_data.tank_player2)
			stage_data.tank_player2.move_right(stage_data.tanksGroup, stage_data.map_stage.brickGroup,
											   	stage_data.map_stage.ironGroup, stage_data.myhome)
			stage_data.tanksGroup.add(stage_data.tank_player2)
			stage_data.player2_moving = True
		# Modified, 2022.01.15, Allow to fire during movement
		# elif key_pressed[pygame.K_KP0]:
		if key_pressed[pygame.K_KP0]:
			if not stage_data.tank_player2.bullet.being:
				sound_data.fire_sound.play()
				stage_data.tank_player2.shoot()


# Used to store sound-related data
class SoundData:
	def __init__(self):
		# Create a new Sound object from a file or buffer object
		self.add_sound = pygame.mixer.Sound("./audios/add.wav")
		self.add_sound.set_volume(1)
		# pygame.mixer.Sound.set_volume: set the play volume of this sound.
		self.bang_sound = pygame.mixer.Sound("./audios/bang.wav")
		self.bang_sound.set_volume(1)
		self.blast_sound = pygame.mixer.Sound("./audios/blast.wav")
		self.blast_sound.set_volume(1)
		self.fire_sound = pygame.mixer.Sound("./audios/fire.wav")
		self.fire_sound.set_volume(1)
		self.Gunfire_sound = pygame.mixer.Sound("./audios/Gunfire.wav")
		self.Gunfire_sound.set_volume(1)
		self.hit_sound = pygame.mixer.Sound("./audios/hit.wav")
		self.hit_sound.set_volume(1)
		self.start_sound = pygame.mixer.Sound("./audios/start.wav")
		self.start_sound.set_volume(1)


# Use to store the data corresponding to each stage
class StageData:
	def __init__(self, num_player, stage):
		# Player number, Level number
		self.num_player = num_player
		self.stage = stage
		# Total number of tanks in the stage (total number of tanks in the enemy's inventory)
		#self.enemytanks_total = min(stage * 18, 80)
		self.enemytanks_total = min(stage * 10, 80) # Maximum number of enemy tanks is 80
		# Total number of enemy tanks present on the map
		self.enemytanks_now = 0
		# Total number of enemy tanks that can exist on the map
		self.enemytanks_now_max = min(max(stage * 2, 4), 8) # Maximum number of enemy tanks on the map is 8
		#self.enemytanks_now_max = min(max(stage * 3, 4), 8)
		# Definition of sprite group
		self.tanksGroup = pygame.sprite.Group()
		self.mytanksGroup = pygame.sprite.Group()
		self.enemytanksGroup = pygame.sprite.Group()
		# commented by iron, 2022.01.15
		# bulletsGroup = pygame.sprite.Group()
		# mybulletsGroup = pygame.sprite.Group()
		self.enemybulletsGroup = pygame.sprite.Group()
		# Store the current randomly generated reward
		self.myfoodsGroup = pygame.sprite.Group()
		# Customized events
		# To create multiple user events with pygame.USEREVENT you need to add 1 to this constant
		# Generate enemy tank events
		self.genEnemyEvent = pygame.constants.USEREVENT
		# If the enemy tank on the map does not reach the maximum, generate an enemy tank every 100ms
		pygame.time.set_timer(self.genEnemyEvent, 100) 
		# Enemy tank stationary recovery event
		# self.recoverEnemyEvent = pygame.constants.USEREVENT   # BUG ?
		self.recoverEnemyEvent = pygame.constants.USEREVENT + 1
		#pygame.time.set_timer(self.recoverEnemyEvent, 8000)
		# Our tank is invincible to recover event
		# self.noprotectMytankEvent = pygame.constants.USEREVENT # BUG ?
		self.noprotectMytankEvent = pygame.constants.USEREVENT + 2
		# pygame.time.set_timer(self.noprotectMytankEvent, 8000)
		# Stage map
		self.map_stage = scene.Map(stage) # Instantiate the Map class, and pass the parameters.
		# Our tank
		self.tank_player1 = tanks.myTank(1) # Instantiate the myTank class, and pass the parameters.
		# modified,  2022.01.15
		self.tank_player2 = tanks.myTank(2) # Instantiate the myTank class, and pass the parameters.
		self.tanksGroup.add(self.tank_player1) # Player tanks add to sprite group.
		self.mytanksGroup.add(self.tank_player1)
		if num_player > 1: # If the number of players is greater than 1, add a second player.
			# tank_player2 = tanks.myTank(2)
			self.tanksGroup.add(self.tank_player2)
			self.mytanksGroup.add(self.tank_player2)
		# Allowing tank track effects
		self.is_switch_tank = True
		# Whether the game player press the arrow keys or not
		self.player1_moving = False
		self.player2_moving = False
		# For the dynamic effect of the tracks
		self.time = 0
		# Enemy tank
		for i in range(0, 3): # i from 0 to 2
			if self.enemytanks_total > 0:
				enemytank = tanks.enemyTank(i) # Enemy tanks are generated from the left, center and right positions.
				self.tanksGroup.add(enemytank)
				self.enemytanksGroup.add(enemytank)
				self.enemytanks_now += 1
				self.enemytanks_total -= 1 # Enemy tank inventory reduced by 1.
		# Home
		self.myhome = home.Home()
		# For enemy tank appearance effects, 3 stars from small to large.
		appearance_img = pygame.image.load("./images/others/appear.png").convert_alpha()
		self.appearances = []
		self.appearances.append(appearance_img.subsurface((0, 0), (48, 48))) # append(): use to add a new element at the end of the list.
		self.appearances.append(appearance_img.subsurface((48, 0), (48, 48)))
		self.appearances.append(appearance_img.subsurface((96, 0), (48, 48)))


# Main function
def main():
	global is_gameover

	pygame.init() # Start pygame module
	pygame.mixer.init() # Initialize the mixer module to load and play sounds.
	screen = pygame.display.set_mode((630, 630)) # Make a window of the desired size (width, height). The return value is a Surface object
	pygame.display.set_caption("坦克大战") #  Set the current window caption
	# Load background image
	bg_img = pygame.image.load("./images/others/background.png")
	# Load music
	sound_data = SoundData()
	# Start interface display
	num_player = show_start_interface(screen, 630, 630)
	# Play the music at the beginning of the game.
    # This function will not affect the interface refresh when playing music.
	"""
	The Sound object can be played using play(). 
    play(loop, maxtime) can take two arguments
    loop is the number of repetitions (1 is twice, note that it is the number of repetitions, not the number of plays), 
    -1 means infinite loop.
    maxtime is the number of milliseconds after which the loop ends.
	"""
	sound_data.start_sound.play()
	# Stage
	stage = 0
	# num_stage = NUM_OF_STAGES
	# Whether the game is over or not
	is_gameover = False
	# Clock
	# Create clock object (control the game cycle frequency)
	clock = pygame.time.Clock()
	# Main loop
	while not is_gameover:
		# Stage
		stage += 1
		if stage > NUM_OF_STAGES:
			break # Jump out of the loop
		show_switch_stage(screen, 630, 630, stage)
		stage_data = StageData(num_player, stage)
		# Main loop of stage
		while True:
			if is_gameover:
				break
			# The number of enemy tanks in stock is 0 and the number of tanks on the map is also 0
			if stage_data.enemytanks_total < 1 and stage_data.enemytanks_now < 1:
				is_gameover = False
				break
			# Handling different events
			for event in pygame.event.get(): # Loop to get events, listen to event state, use get() to get events
				if event.type == pygame.QUIT:
					"""
					When the close window event is obtained, pygame.quit() is executed to exit the window.
     				At this point, although the window is destroyed, the console program is still in a dead loop, 
          			so use sys.exit() to exit the program.
					"""
					pygame.quit() # pygame.quit uninstall the imported pygame module, close the window
					sys.exit() # The program exits directly, without catching exceptions
				# Generate a new enemy tank
				if event.type == stage_data.genEnemyEvent: # Get generate a new enemy tank event
					if stage_data.enemytanks_total > 0: # The number of enemy tanks in stock is greater than 0
						if stage_data.enemytanks_now < stage_data.enemytanks_now_max: # The number of enemy tanks on map is less than the maximum
							enemytank = tanks.enemyTank() # Instantiated object
							if not pygame.sprite.spritecollide(enemytank, stage_data.tanksGroup, False, None): # Generated enemy tanks do not collide with all other tanks
								stage_data.tanksGroup.add(enemytank) # Generate new enemy tanks
								stage_data.enemytanksGroup.add(enemytank)
								stage_data.enemytanks_now += 1
								stage_data.enemytanks_total -= 1
				# Allow stationary enemy tanks to move
				if event.type == stage_data.recoverEnemyEvent:
					for each in stage_data.enemytanksGroup:
						each.can_move = True # Each sprite (enemy tank) in enemytanksGroup is restored to movement
				# Time is up, our tank lost its protect mask.
				if event.type == stage_data.noprotectMytankEvent:
					for each in stage_data.mytanksGroup:
						# BUG
						#stage_data.mytanksGroup.protected = False
						each.protected = False # Each of our tanks in mytanksGroup loses its protect mask.
			# Listening to user keyboard operations
			# pygame.key.get_pressed()
			# Returns a series of boolean values indicating the state of each key on the keyboard. 
   			# Use the key constant values to index the array. A True value indicates that the button is pressed.
			key_pressed = pygame.key.get_pressed()

			# Handling player 1 related keyboard events.
			handle_player1_events(key_pressed, sound_data, stage_data)

			# Handling player 2 related keyboard events.
			handle_player2_events(key_pressed, sound_data, stage_data)

			# Redraw the entire interface.
			# Set the background image.
			screen.blit(bg_img, (0, 0))
            # Each sprite of the sprite group (coordinates defined in scene.stage()) is drawn on the map
			# Brick walls
			for each in stage_data.map_stage.brickGroup:
				screen.blit(each.brick, each.rect)
			# Iron walls
			for each in stage_data.map_stage.ironGroup:
				screen.blit(each.iron, each.rect)
			# Ice
			for each in stage_data.map_stage.iceGroup:
				screen.blit(each.ice, each.rect)
			# River
			for each in stage_data.map_stage.riverGroup:
				screen.blit(each.river, each.rect)
			# Tree
			for each in stage_data.map_stage.treeGroup:
				screen.blit(each.tree, each.rect)
			# Allow is_switch_tank to flip once in every 5 ticks to achieve dynamic enemy tank tracks
			stage_data.time += 1
			if stage_data.time == 5:
				stage_data.time = 0
				stage_data.is_switch_tank = not stage_data.is_switch_tank
			# Call to implement our tank track dynamic effect and protect mask effect.
			handle_mytanksGroup(stage_data, screen)
			# Call to implement enemy tank birth effect and track dynamic effect.
			handle_enemytanksGroup(stage_data, screen)
			# Call to implement various collision events of our bullets
			handle_mybullet(stage_data, sound_data, screen)
			# Call to implement various collision events of enemy bullets
			handle_enemy_bullet(stage_data, sound_data, screen)
			# Home image is drawn on the map
			screen.blit(stage_data.myhome.home, stage_data.myhome.rect)
			# Call to implement the effect of food
			handle_food(stage_data, sound_data, screen)

			if stage_data.num_player == 1:
				"""
				A simple field name in numeric form is equivalent to treating all the positional parameters in format as a whole as a tuple, 
    			and taking the values by the numbers in the field name
				i.e. {0} is equivalent to tuple[0], so the numbers inside the brackets cannot be out of bounds
    			"""
				pygame.display.set_caption("坦克大战: 第{0}关, 我方库存坦克数 {1}, 敌方库存坦克数 {2}".format(
									stage_data.stage,
									stage_data.tank_player1.life,
									stage_data.enemytanks_total))
			else:
				pygame.display.set_caption("坦克大战: 第{0}关, 我方库存坦克数 ({1},{2}), 敌方库存坦克数 {3}".format(
									stage_data.stage,
									stage_data.tank_player1.life, stage_data.tank_player2.life,
									stage_data.enemytanks_total))
			pygame.display.flip() # pygame.display.flip(): update the entire surface to be displayed
			"""
			clock.tick() is generally set in the loop to limit the number of cycles per second in the loop. 
   			Thus, the effect of setting the page refresh rate is achieved.
			clock.tick(60) is to refresh the page 60 times in one second.
   			"""
			clock.tick(60)
	if not is_gameover:
		# If players are win, screen displays "恭喜通关!".
		show_end_interface(screen, 630, 630, True)
	else:# If players are not win, screen displays "game over".
		show_end_interface(screen, 630, 630, False)


if __name__ == '__main__':
	main()


