import pygame
import random
pygame.init()
# Define some colors
BLACK = (0, 0, 0)
BLUE = (0,0,255)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GRAY = (119,118,110)
missilesList = []
tractorList = []
E1 = []
# Set the width and height of the screen [width, height]
display_width = 800
display_height = 600
gamedisplays = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption("Space Wars")
clock = pygame.time.Clock()
spaceship = pygame.image.load('spaceship.png').convert_alpha()
spaceshipPosition = [display_width*0.4, display_height*0.8]
#spaceship = pygame.transform.scale(spaceship)
missileImage = pygame.image.load('missile.png').convert_alpha()
lastFired = 0
rpm = 180
space = pygame.image.load("space background.jpg")
beam = pygame.image.load("beam.png").convert_alpha()
initialbackground = pygame.image.load("initial background.png")
flash = pygame.image.load("flash.png")
initial = 0
class missileClass:
    def __init__(self, position):
        self.position = position
        self.cycles = 0

class tractorClass:
    def __init__(self,position):
        self.position = position
        self.cycles = 0
class enemyship:
    def __init__(self, position):
        self.position = position

def intro():
	#pygame.mixr.Sound.play(start_music)
	intro = True
	menu1_x = 200
	menu1_y = 400
	menu2_x = 500
	menu2_y = 400
	menu_width = 100
	menu_height = 50
	while intro:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
		pygame.display.set_icon(spaceship)
		
		pygame.draw.rect(gamedisplays,BLACK,(200,400,100,50))
		pygame.draw.rect(gamedisplays,BLACK,(500,400,100,50))
			
		gamedisplays.blit(initialbackground, (0,0))
		font = pygame.font.SysFont ("Arial", 72)
		text = font.render("Hello!", True, (WHITE))
		pygame.draw.rect(gamedisplays,GREEN,(200,400,100,50))
		pygame.draw.rect(gamedisplays,RED,(500,400,100,50))
		
		mouse = pygame.mouse.get_pos()
		click = pygame.mouse.get_pressed()
		
		
		if menu1_x < mouse[0] < menu1_x+menu_width and menu1_y < mouse[1] < menu1_y+menu_height:
			pygame.draw.rect(gamedisplays,BLUE,(200,400,100,50))
			if click[0] == 1:
				intro = False
		if menu2_x < mouse[0] < menu2_x+menu_width and menu2_y < mouse[1] < menu2_y+menu_height:
			pygame.draw.rect(gamedisplays,BLUE,(500,400,100,50))
			if click[0] == 1:
				pygame.quit()
				quit()
	
		message_display("Go",40,menu1_x+menu_width/2,menu1_y+menu_height/2)
		message_display("Exit",40,menu2_x+menu_width/2,menu2_y+menu_height/2)
		
		pygame.display.update()
		clock.tick(50)


def message_display(text,size,x,y):
	font = pygame.font.Font("freesansbold.ttf",size)
	text_surface , text_rectangle = text_objects(text,font)
	text_rectangle.center =(x,y)
	gamedisplays.blit(text_surface,text_rectangle)


def text_objects(text,font):
	textSurface = font.render(text,True,BLACK)
	return textSurface,textSurface.get_rect()


def crash():
    message_display("You Died")

def load_image(x , y, image_name):
    img = pygame.image.load(image_name)
    gamedisplays.blit(img, (x, y))

def game_loop():
    x_change = 5
    missile_v = -10
    thing_width = 70
    thing_height = 140
    thing_startx = random.randrange(0, 125)
    thing_startx1 = random.randrange(175, 300)
    thing_startx2 = random.randrange(305, 450)
    thing_starty1 = -5
    thing_starty = -5
    thing_speed = random.randrange(1,5)
    thing_speed1 = random.randrange(1, 10)
    bumped = False
    isFiring = False
    global lastFired
    while not bumped:
        # --- Main event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                     bumped = True


            pressed = pygame.key.get_pressed()
            isFiring = False
            if pressed[pygame.K_LEFT]:
                if spaceshipPosition[0] > 0:
                    spaceshipPosition[0] -= x_change
            if pressed[pygame.K_RIGHT]:
                if spaceshipPosition[0] < display_width-100:
                    spaceshipPosition[0] += x_change
            if pressed[pygame.K_UP]:
                if pygame.time.get_ticks()-lastFired >=60000/rpm:
                    lastFired =pygame.time.get_ticks()
                    newMissile = missileClass([spaceshipPosition[0]+55, spaceshipPosition[1]])
                    missilesList.append(newMissile)
                    isFiring = True
            if pressed[pygame.K_DOWN]:

                if len(tractorList) == 0:
                    lasttracted =pygame.time.get_ticks()
                    newTractor = tractorClass([spaceshipPosition[0]+67, spaceshipPosition[1]])
                    tractorList.append(newTractor)
            if pygame.time.get_ticks()-lastFired >=60000/rpm:
                    lastFired =pygame.time.get_ticks()
                    newMissile = enemyship1([spaceshipPosition[0]+55, spaceshipPosition[1]])
                    E1.append(newMissile)

            gamedisplays.blit(space, (0,0))
            for i in missilesList:
                if i.cycles < 300:
                    gamedisplays.blit(missileImage, [i.position[0]-missileImage.get_rect().width/2+183, i.position[1]])
                    i.position[1] += missile_v
                    i.cycles += 1
            for i in tractorList:
                if i.cycles < 2:
                    gamedisplays.blit(flash, [i.position[0] - 4* flash.get_rect().width / 9+2,
                                              i.position[1] - flash.get_rect().height / 2])
                    gamedisplays.blit(beam, [i.position[0]-beam.get_rect().width/2+8, i.position[1]-beam.get_rect().height])

                    i.cycles += 1
                else:
                    tractorList.remove(i)

            gamedisplays.blit(spaceship, spaceshipPosition)

            global initial
            if initial <500:
                thing_starty += thing_speed
                load_image(thing_startx, thing_starty, 'enemyship1.png')
                initial += 1
            else:
                thing_starty = -5
                thing_startx = random.randint(1,480)
                load_image(thing_startx, thing_starty, 'enemyship1.png')
                initial = 1


            pygame.display.update()
            clock.tick(60)

intro()
game_loop()
pygame.quit()
quit()
