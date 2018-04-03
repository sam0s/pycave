#sam0s
#very sloppy way to view mazeGen.py results

import pygame
import assets.mazeGen as mazeGen
from pygame.locals import *

display = pygame.display.set_mode((640,480))

def main2():
    go=1
    maze,startpos,endpos=mazeGen.generate(25)
    #print(maze)
    #startpos=endpos=(0,0)
    mazesurf=pygame.Surface((640,480))
    mazesurf.fill((255,255,255))

    x=0
    y=0

    #print(endpos)
    #print(maze[endpos[1]][endpos[0]])

    #green-start red-end blue-crate purp-enemy

    pygame.draw.rect(mazesurf,(0,255,0),(startpos[0]*16,startpos[1]*16,16,16),0)

    for row in maze:
        for col in row:
            if col==0:pygame.draw.rect(mazesurf,(0,0,0),(x*16,y*16,16,16),0)
            if col==3:pygame.draw.rect(mazesurf,(100,100,250),(x*16,y*16,16,16),0)
            if col==4:pygame.draw.rect(mazesurf,(255,100,250),(x*16,y*16,16,16),0)
            x+=1
        x=0
        y+=1
    pygame.draw.rect(mazesurf,(255,0,0),(endpos[0]*16,endpos[1]*16,16,16),0)


    while go==1:
        display.fill((255,255,255))
        display.blit(mazesurf,(0,0))

        pygame.display.flip()

        for e in pygame.event.get():
            if e.type == MOUSEBUTTONDOWN:
                mse=pygame.mouse.get_pos()
                mse16=(int((mse[0])/16)*16, int((mse[1])/16)*16)
                print(int(mse16[0]/16),int(mse[1]/16))
            if e.type == KEYDOWN:
                main2()
            if e.type == QUIT:
                pygame.display.quit()
                go=-1



if __name__ == "__main__":
    main2()
