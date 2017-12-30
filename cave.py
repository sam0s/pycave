import pygame
from pygame import *
from time import sleep

GAME_WIDTH = 640
GAME_HEIGHT = 480

window = pygame.display.set_mode((GAME_WIDTH,GAME_HEIGHT))
screen = pygame.Surface((GAME_WIDTH,GAME_HEIGHT))

class Entity(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

class genCollide(Entity):
    def __init__(self,x,y):
        Entity.__init__(self)
        self.image = Surface((64,64))
        self.rect = Rect(x,y,64,64)

class caveBlock(Entity):
    def __init__(self,x,y):
        Entity.__init__(self)
        self.image = Surface((16,16));self.image.fill((100,100,100))
        self.rect = Rect(x,y,16,16)

blocklist=pygame.sprite.Group()

carve=genCollide(32,32)


for a in range(GAME_HEIGHT/16):
    for f in range(GAME_WIDTH/16):
        blocklist.add(caveBlock(f*16,a*16))

pygame.sprite.spritecollide(carve, blocklist, True)

blocklist.draw(screen)

window.blit(screen,(0,0))

pygame.display.flip()

sleep(3)
