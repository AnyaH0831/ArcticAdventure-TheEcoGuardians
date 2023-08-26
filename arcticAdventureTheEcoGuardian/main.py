#Arctic Adventure: The EcoGuardians
#The imports
import os
import pygame
import random
import math
from os import listdir
from os.path import isfile, join
pygame.init()

pygame.display.set_caption("Arctic Adventure: The EcoGuardians")

#Global Variables
size = (800, 500)
FPS = 30  #Frames per second
CHARACTER_VEL = 5  #velocity

RED=(255,0,0)
GREEN=(0,255,0)
BLUE=(0,0,255)
WHITE=(247,247,242)
BLACK=(0,0,0)
GREY = (100,100,100) 
DARKBLUE = (16, 64, 143)
LIGHTBLUE = (144, 191, 224)


firstFont = pygame.font.SysFont("Times New Roman",25)
lazyBearFont = pygame.font.Font("lazyBear.ttf", 35)
bigLazyBearFont = pygame.font.Font("lazyBear.ttf", 60)
bubbleGumFont = pygame.font.Font("Bubblegum.ttf", 25)

screen = pygame.display.set_mode(size)

clock=pygame.time.Clock()

fishCount=0


menuBG=pygame.image.load('menuBG.webp')
menuBG=pygame.transform.scale(menuBG,(menuBG.get_width()*800/menuBG.get_width(),menuBG.get_height()*800/menuBG.get_width()))

gameBG=pygame.image.load('gameBG.jpeg')
gameBG=pygame.transform.scale(gameBG,(800,500))

fishPic=pygame.image.load('fish.png').convert_alpha()
fishPic=pygame.transform.scale(fishPic,(fishPic.get_width()*2,fishPic.get_height()*2))

iglooPic=pygame.image.load('igloo.png')


def drawButton(rect,word,colourBase,colourWord,drawFont):  #a function used to draw all the functions in the game

  pygame.draw.rect(screen,colourBase,rect) #draw the rectangle of the button

  textWidth, textHeight = drawFont.size(word) #centre the texts
  start = drawFont.render(word,1,colourWord)
  inX = (rect[2] - textWidth)//2
  inY = (rect[3] - textHeight)//2

  screen.blit(start,(rect[0]+inX,rect[1]+inY))  #display
  pygame.draw.rect(screen,WHITE,rect,2) #draw the border
  
  
def drawMenu():  #Draw menu page
  global state,mX,mY,JUMPING,keyDown1,character,offsetX,offsetY
  state = 0
  # screen.blit(backgroundPic,(0,0))
  # screen.blit(backgroundPicFlip,(backgroundPic.get_width(),0))

  screen.blit(menuBG,(0,0))
  title = bigLazyBearFont.render("Arctic Adventure:",1,DARKBLUE)
  title2 = bigLazyBearFont.render("The EcoGuardian",1,DARKBLUE)
  screen.blit(title,(75,55,100,50))  #display
  screen.blit(title2,(100,105,100,50))
  
  #buttons
  rectMenu=[] #rects for the pos of buttons
  for h in range(2):
    rectMenu+=[pygame.Rect(535,300+h*55,175,50)]
  wordMenu=['START','EXIT']#words on the button
  stateMenu=[1,4]#state for buttons
  for i in range(2):
     if rectMenu[i].collidepoint(mX,mY) == True: #check collision with a button
        drawButton(rectMenu[i],wordMenu[i],LIGHTBLUE,DARKBLUE,bubbleGumFont) #change colour of the button
        if eButton == 1:  #if user click; start game
          state = stateMenu[i]

          mX,mY=0,0
          JUMPING = False
          keyDown1 = False
          character = Character(0,200,50,50)
          offsetX=0
          offsetY=0

     else:
        drawButton(rectMenu[i],wordMenu[i],DARKBLUE,WHITE,bubbleGumFont)

 

#-----------------------------------------------------------
#tt

def drawGame(window,character,objects, waterObjects, offsetX,offsetY):
  global state
  state=1
 

  if offsetX<0:
    gameBGX=((offsetX*-1)%800)*-1

  else:
    gameBGX=(offsetX%800)


  screen.blit(gameBG,(((-1)*(gameBGX)),0))

  screen.blit(gameBG,(800-gameBGX,0))

  screen.blit(gameBG,(((-1)*(800))-gameBGX,0))


  
  for obj in objects:
    obj.draw(window,offsetX,offsetY)
    
  for obj in waterObjects:
    obj.draw(window,offsetX,offsetY)
    
  screen.blit(iglooPic,(-offsetX,360-iglooPic.get_height()-offsetY))


  for i in range(75):
    if i%2==0:
      colourStrip=WHITE
    else:
      colourStrip=RED
    pygame.draw.rect(screen,colourStrip,(-1610-offsetX, i*20-offsetY-500,5,20))

  
  character.draw(window,offsetX,offsetY)
  if character.rect.x<-1680 and character.rect.y>=360:
    state=STATE_WIN
  screen.blit(iglooPic,(-1750-offsetX,490-iglooPic.get_height()-offsetY))


#-----------------------------------------------------------
  
def drawWin():

  global state,mX,mY,JUMPING,keyDown1,character,offsetX,offsetY
  state=STATE_WIN

  rect1 = pygame.Rect(250,300,100,30)  #button rectangles
  rect2 = pygame.Rect(450,300,100,30)

  pygame.draw.rect(screen,LIGHTBLUE,(100,100,600,300))  #draw the pop-up
  pygame.draw.rect(screen,WHITE,(100,100,600,300),3)

  drawButton(rect1,"YES",DARKBLUE,WHITE,bubbleGumFont)  #draw button of yes or no
  drawButton(rect2,"NO",DARKBLUE,WHITE,bubbleGumFont)

  lost = bubbleGumFont.render("YOU WIN!",1,DARKBLUE)   
  screen.blit(lost,(330,200))  #display

  replay = bubbleGumFont.render("Do you want to replay?",1,DARKBLUE)  
  screen.blit(replay,(250,235))  #display
  
  if rect1.collidepoint(mX,mY) == True:  #check collision
    drawButton(rect1,"YES",LIGHTBLUE,DARKBLUE,bubbleGumFont)
    if eButton == 1: #left click
      state = STATE_GAME # game

      mX,mY=0,0
      JUMPING = False
      keyDown1 = False
      character = Character(0,200,50,50)
      offsetX=0
      offsetY=0
    
  elif rect2.collidepoint(mX,mY) == True:
    drawButton(rect2,"NO",LIGHTBLUE,DARKBLUE,bubbleGumFont)
    if eButton == 1:
      state = STATE_MAIN #go back to main page

#-----------------------------------------------------------

def drawLose():
  global state,mX,mY,JUMPING,keyDown1,character,offsetX,offsetY
  state=STATE_LOSE

  rect1 = pygame.Rect(250,300,100,30)  #button rectangles
  rect2 = pygame.Rect(450,300,100,30)

  pygame.draw.rect(screen,LIGHTBLUE,(100,100,600,300))  #draw the pop-up
  pygame.draw.rect(screen,WHITE,(100,100,600,300),3)

  drawButton(rect1,"YES",DARKBLUE,WHITE,bubbleGumFont)  #draw button of yes or no
  drawButton(rect2,"NO",DARKBLUE,WHITE,bubbleGumFont)

  lost = bubbleGumFont.render("YOU LOST!",1,DARKBLUE)   
  screen.blit(lost,(330,200))  #display

  replay = bubbleGumFont.render("Do you want to replay?",1,DARKBLUE)  
  screen.blit(replay,(250,235))  #display
  
  if rect1.collidepoint(mX,mY) == True:  #check collision
    drawButton(rect1,"YES",LIGHTBLUE,DARKBLUE,bubbleGumFont)
    if eButton == 1: #left click
      state = STATE_GAME # game

      mX,mY=0,0
      JUMPING = False
      keyDown1 = False
      character = Character(0,200,50,50)
      offsetX=0
      offsetY=0
    
  elif rect2.collidepoint(mX,mY) == True:
    drawButton(rect2,"NO",LIGHTBLUE,DARKBLUE,bubbleGumFont)
    if eButton == 1:
      state = STATE_MAIN #go back to main page


#-----------------------------------------------------------

def drawExit():
  global state, run
  state=4
  
  rect1 = pygame.Rect(250,300,100,30)  #button rectangles
  rect2 = pygame.Rect(450,300,100,30)

  pygame.draw.rect(screen,LIGHTBLUE,(100,100,600,300))  #draw the pop-up
  pygame.draw.rect(screen,WHITE,(100,100,600,300),3)

  drawButton(rect1,"YES",DARKBLUE,WHITE,bubbleGumFont)  #draw button of yes or no
  drawButton(rect2,"NO",DARKBLUE,WHITE,bubbleGumFont)

  exit = bubbleGumFont.render("Do you want to exit?",1,DARKBLUE)   #ask if want to exit

  screen.blit(exit,(260,200))  #display

  if rect1.collidepoint(mX,mY) == True:  #check collision
    drawButton(rect1,"YES",LIGHTBLUE,DARKBLUE,bubbleGumFont)
    if eButton == 1: #left click
      run = False  #stop loop
  elif rect2.collidepoint(mX,mY) == True:
    drawButton(rect2,"NO",LIGHTBLUE,DARKBLUE,bubbleGumFont)
    if eButton == 1:
      state = STATE_MAIN #go back to main page



def flip(sprites):
  return[pygame.transform.flip(sprite,True,False) for sprite in sprites]


def load_sprite_sheets(dir1,width,height,direction=False):
  path=dir1
  images=[f for f in listdir(path) if isfile(join(path,f))]
  all_sprites={}
  for image in images:
    sprite_sheet = pygame.image.load(join(path, image)).convert_alpha()

    sprites = []
    for i in range(sprite_sheet.get_width() // width):
      surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
      rect = pygame.Rect(i * width, 0, width, height)
      surface.blit(sprite_sheet, (0, 0), rect)
      sprites.append(pygame.transform.scale_by(surface,3))
      # sprites.append(pygame.transform.scale2x(surface))


    if direction:
      all_sprites[image.replace(".png", "") + "_right"] = sprites
      all_sprites[image.replace(".png", "") + "_left"] = flip(sprites)
    else:
      all_sprites[image.replace(".png", "")] = sprites

  return all_sprites






def get_block(size,image):
  path = join("Tiles",image)
  image = pygame.image.load(path).convert_alpha()
  surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
  rect = pygame.Rect(0, 0, size, size)
  surface.blit(image, (0, 0), rect)
  return surface



class Character(pygame.sprite.Sprite):

  GRAVITY=1
  ANIMATION_DELAY = 7
  
  SPRITES=load_sprite_sheets('polarBearPic',32,32,True)
  def __init__(self,x,y,width,height):
    super().__init__()
    self.rect = pygame.Rect(x,y,width,height)
    self.x_vel = 0
    self.y_vel = 0
    self.y_velW = 0
    self.mask = None
    self.direction = "left"
    self.animation_count = 0
    self.fall_count = 0

    self.jump_count = 0

  @staticmethod
  def setGravity(gravity):
    Character.GRAVITY = gravity
  
  def move(self, dx, dy):
    self.rect.x += dx
    self.rect.y += dy

  def move_left(self,vel):
    self.x_vel = -vel
    if self.direction != "left":
      self.direction = "left"
      self.animation_count = 0

  def move_right(self,vel):
    self.x_vel = vel
    if self.direction != "right":
      self.direction = "right"
      self.animation_count = 0

  # def move_up(self,vel):
  #   self.y_velW = -vel
    
      
  # def move_down(self,vel):
  #   self.y_velW = vel
    
  def loop(self,fps,apply_gravity=True):

    if apply_gravity:
      self.y_vel += min(1,self.fall_count*self.GRAVITY/FPS)
    else:
      self.y_vel = 0.5
      
    # self.y_vel += min(1,self.fall_count*self.GRAVITY/FPS)
    if self.y_velW != 0:
      self.move(self.x_vel,self.y_velW)
    else:
      self.move(self.x_vel,self.y_vel)

    self.fall_count += 1
    self.update_sprite()


  def update_sprite(self):

    sprite_sheet = "idle"
    if (self.y_vel < 0 and self.jump_count != 0) or self.y_vel>self.GRAVITY*2:
      sprite_sheet = "jump"
 
    elif self.x_vel != 0:
      sprite_sheet = "move"

    # elif waterCollide(character, waterObjects):
    #   print('')
    #   sprite_sheet='swim'

    
    sprite_sheet_name = sprite_sheet + "_" + self.direction
    sprites = self.SPRITES[sprite_sheet_name]
    sprite_index = (self.animation_count//self.ANIMATION_DELAY) % len(sprites)
    self.sprite = sprites[sprite_index]
    self.animation_count += 1
    self.update()


  def update(self):
    self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
    self.mask = pygame.mask.from_surface(self.sprite)  #allows perfect collision
    
  def jump(self):
    self.y_vel = -self.GRAVITY * 11
    self.animation_count = 0
    self.jump_count += 1
    if self.jump_count == 1:
      self.y_vel = -self.GRAVITY * 6
      self.fall_count = 0

  def landed(self):
    self.fall_count = 0
    self.y_vel = 0
    self.jump_count = 0

  def hit_head(self):
    self.count = 0
    self.y_vel *= -1
  
  def draw(self,window,offsetX,offsetY):
    # self.sprite = self.SPRITES['idle_'+self.direction][0]
    window.blit(self.sprite,(self.rect.x - offsetX,self.rect.y-offsetY))





class Object(pygame.sprite.Sprite):
  #constructor
  def __init__(self, x, y, width, height, name=None):
    super().__init__()
    self.rect = pygame.Rect(x, y, width, height)
    self.image = pygame.Surface((width, height), pygame.SRCALPHA)
    self.width = width
    self.height = height
    self.name = name

  def draw(self, window,offsetX,offsetY):
    window.blit(self.image, (self.rect.x-offsetX, self.rect.y-offsetY))


class Block(Object):
  def __init__(self, x, y, size,blockImage):
    super().__init__(x, y, size, size)
    block = get_block(size,blockImage)
    self.image.blit(block, (0, 0))
    self.mask = pygame.mask.from_surface(self.image)
    self.__blockType = blockImage

  def getBlockType(self):
  
    return self.__blockType
    

def check_vertical_collision(character,objects, dy):
  collided_objects = []
  for obj in objects:
    if pygame.sprite.collide_mask(character,obj):
      if dy > 0:
        character.rect.bottom = obj.rect.top
        character.landed()
      elif dy < 0:
        character.rect.top = obj.rect.bottom
        character.hit_head()
    collided_objects.append(obj)

  return collided_objects


def collide(character,objects,dx,dy):
  character.move(dx,dy)
  character.update()

  collided_object = None
  
  for obj in objects:
    if pygame.sprite.collide_mask(character,obj):
      collided_object = obj
      break

  character.move(-dx,0)
  character.update()
  return collided_object

def waterCollide(character,objects):

  ifCollideWater = False
  
  for obj in objects:
    if pygame.sprite.collide_mask(character,obj):

      if obj.getBlockType() == "iceWaterMid.png" or obj.getBlockType() == "iceWaterDeep.png":
        ifCollideWater = True
        break
        

  return ifCollideWater





def check_move(character, objects):
  keys = pygame.key.get_pressed()

  character.x_vel = 0
  character.y_velW = 0

  collide_left = collide(character, objects, - CHARACTER_VEL*5,0)
  collide_right = collide(character, objects, CHARACTER_VEL*5,0)
  # collide_down = collide(character, objects, 0, CHARACTER_VEL*5)

  if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and not collide_right:
    character.move_right(CHARACTER_VEL)
  elif (keys[pygame.K_LEFT] or keys[pygame.K_a]) and not collide_left:
    character.move_left(CHARACTER_VEL)
  # if waterCollide(character,objects) ==True and (keys[pygame.K_DOWN] or keys[pygame.K_s]) and not collide_down:
  #   character.move_down(CHARACTER_VEL)
  check_vertical_collision(character,objects,character.y_vel)


#The states
STATE_MAIN = 0
STATE_GAME = 1
STATE_WIN = 2
STATE_LOSE = 3
STATE_EXIT = 4

mX,mY=0,0
eButton=0
JUMPING = False
keyDown1 = False
character = Character(0,200,50,50)
offsetX=0
offsetY=0

fishX=[70]
fishY=[-30]

#current state
state = STATE_MAIN

myClock = pygame.time.Clock()  #time
run = True

  
block_size = 70
# ground = [Block(i*block_size,500-block_size,block_size,"tundra.png") for i in range(-800//block_size,(800*2)//block_size)]

blocks = [Block(0,500-block_size,block_size,"tundra.png")]

tundra1 = []
water = []
deepWater = []
for i in range(4):
  tundra1 += [Block(i*block_size,150,block_size,"tundra.png")]
  tundra1 += [Block(-70,150+(i*block_size),block_size,"tundra.png")]
  tundra1 += [Block(i*block_size-350,150+(i*block_size),block_size,"tundra.png")]


for i in range(8):
  tundra1 += [Block(i*block_size-910,290,block_size,"tundra.png")]

  tundra1 += [Block(-980,-200+(i*block_size),block_size,"tundra.png")]


for j in range(5):
  water += [Block(j*block_size-770,80,block_size,"iceWaterMid.png")]
  tundra1 += [Block(j*block_size-770,150,block_size,"tundra.png")]



deepWater += [Block(i*block_size,560,block_size,"iceWaterDeep.png") for i in range(-1500//block_size,(800*2)//block_size)]
deepWater += [Block(i*block_size,630,block_size,"iceWaterDeep.png") for i in range(-1500//block_size,(800*2)//block_size)]


# water += [Block(i*block_size,490,block_size,"iceWaterMid.png") for i in range(-1500//block_size,(800*2)//block_size)]

for j in range(3):
  deepWater += [Block(i*block_size,490+j*70,block_size,"iceWaterDeep.png") for i in range(-60//block_size,(400*2)//block_size)]



water += [Block(i*block_size,420,block_size,"iceWaterMid.png") for i in range(-60//block_size,(400*2)//block_size)]

for i in range(3):
  water += [Block(i*block_size-280,150,block_size,"iceWaterMid.png")]
  # tundra1 += [Block(i*block_size-350,420,block_size,"tundra.png")]
  
  tundra1 += [Block(-420,10+(i*block_size),block_size,"tundra.png")]
  tundra1 += [Block(-1470+i*block_size,-60,block_size,"tundra.png")]

  
  for j in range(i):
    deepWater += [Block(i*block_size-280,(j+3)*block_size+10,block_size,"iceWaterDeep.png")]


for i in range(2):
  tundra1 += [Block(-840,80+(i*block_size),block_size,"tundra.png")]
  tundra1+=[Block(-1190,80+(i*block_size*4),block_size,"tundra.png")]
  tundra1+=[Block(-1750+i*block_size,490,block_size,"tundra.png")]
  # tundra1 += [Block(i*block_size-280,290,block_size,"tundra.png")]

for i in range(13):
  tundra1 +=[Block(i*block_size-1050,490,block_size,"tundra.png")]

#
tundra1 += [Block(-140,490,block_size,"tundra.png")]
objects = [Block(0,500-block_size*2,block_size,"tundra.png"),Block(70,500-block_size*2,block_size,"tundra.png"),Block(block_size*3,500-block_size*5,block_size,"tundra.png"),Block(block_size*5,500-block_size*3,block_size,"tundra.png"),Block(-1050,220,block_size,"tundra.png"),*tundra1]

waterObjects = [*water,*deepWater]



scroll_area_width=200
scroll_area_height=200



while run:
  eButton = 0 # reset button to 0
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      run = False
      break
    
    if event.type == pygame.KEYDOWN:
      
      if (event.key == pygame.K_SPACE or event.key == pygame.K_w or event.key == pygame.K_UP) and character.jump_count < 2:
        character.jump()


     
    if event.type == pygame.MOUSEBUTTONDOWN:       
      eButton = event.button
    if event.type == pygame.MOUSEMOTION:
      mX,mY=event.pos

  if state == STATE_MAIN: 
    drawMenu()
    
  if state == STATE_GAME:  
    character.loop(FPS,apply_gravity=True)
    check_move(character,objects)
    
    drawGame(screen,character,objects,waterObjects,offsetX,offsetY)

    
    

    
    # for i in range(len(fishX)):
      
    #   fishMask=pygame.mask.from_surface(fishPic)
    #   fishRect=fishPic.get_rect()
    #   # screen.blit(maskPic,(locate))
      
    #   if pygame.sprite.collide_mask(character,fishMask):
    #     print(fishCount)
    #     fishCount+=1
    #     # fishPos.remove(locate)

  # for obj in objects:
  #   if pygame.sprite.collide_mask(character,obj):

  #     if obj.getBlockType() == "iceWaterMid.png" or obj.getBlockType() == "iceWaterDeep.png":
  #       ifCollideWater = True
  #       break



    
    # screen.blit(fishPic,(70-offsetX,-30-offsetY))
    ifWaterCollide = waterCollide(character, waterObjects)

    if ifWaterCollide==True:
      state = STATE_LOSE

    

    
    if ((character.rect.right - offsetX >= 800 - scroll_area_width) and character.x_vel > 0) or ((character.rect.left - offsetX <= scroll_area_width) and character.x_vel < 0):
      offsetX += character.x_vel

    if ((character.rect.bottom - offsetY >= 500 - scroll_area_height) and character.y_vel > 0) or ((character.rect.top - offsetY <= scroll_area_height) and character.y_vel < 0):
      offsetY += character.y_vel

  
  if state == STATE_WIN:
    drawWin()
  if state == STATE_LOSE:
    drawLose()
  if state == STATE_EXIT:
    drawExit()

  pygame.display.flip()
  myClock.tick(FPS) #time 

pygame.quit()
