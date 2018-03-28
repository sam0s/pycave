#sam0s
#very sloppy way to view mazeGen.py results

import pygame,mazeGen
from pygame.locals import *

display = pygame.display.set_mode((640,480))

def main2():
    go=1
    maze,startpos,endpos=mazeGen.generate(27)
    #print(maze)
    #print(startpos)
    mazesurf=pygame.Surface((640,480))
    mazesurf.fill((255,255,255))
    pygame.draw.rect(mazesurf,(0,255,0),(startpos[0]*16,startpos[1]*16,16,16),0)
    x=0
    y=0
    for row in maze:
        for col in row:
            if col==0:pygame.draw.rect(mazesurf,(0,0,0),(x*16,y*16,16,16),0)
            if col==3:pygame.draw.rect(mazesurf,(100,100,250),(x*16,y*16,16,16),0)
            x+=1
        x=0
        y+=1
    pygame.draw.rect(mazesurf,(255,0,0),(endpos[0]*16,endpos[1]*16,16,16),0)




    while go==1:
        display.fill((255,255,255))
        display.blit(mazesurf,(0,0))

        pygame.display.flip()

        for e in pygame.event.get():
            if e.type == QUIT:
                pygame.display.quit()
                go=-1



if __name__ == "__main__":
    main2()
