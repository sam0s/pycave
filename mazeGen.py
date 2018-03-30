import random

def generate(size):
    random.seed(22)
    go=1
    size=size

    cellList=[]
    maze=[]

    for numb in range(size):
        maze.append([0]*(size))
    maze=padMaze(maze,size)
    startpos=(random.randrange(0,size),random.randrange(0,size))
    endpos=(0,0)
    maze[startpos[1]][startpos[0]]=1

    #right,down,left,up
    dx=[1,0,-1,0]
    dy=[0,1,0,-1]
    #cell count
    cc=0
    for cell in range(4):
        cellCheck=maze[startpos[1]+dy[cc]][startpos[0]+dx[cc]]
        if cellCheck == 0:
            cellList.append((startpos[0]+dx[cc],startpos[1]+dy[cc]))
        cc+=1

    while len(cellList)>0:

        #confirm adrules
        good=0
        timeout=0
        while good<1:
            timeout+=1
            adjacents=0
            chosenID=random.randint(0,len(cellList)-1)
            chosen=cellList[chosenID]
            cc=0
            for cell in range(4):
                cellCheck=maze[chosen[1]+dy[cc]][chosen[0]+dx[cc]]
                if cellCheck == 1:
                    adjacents+=1
                cc+=1
            if adjacents<=1:
                good=2
            if timeout>999:
                good=2
                cellList=[]


        if len(cellList)>0:
            maze[chosen[1]][chosen[0]]=1
            endpos=(chosen[0],chosen[1])
            cc=0
            for cell in range(4):
                cellCheck=maze[chosen[1]+dy[cc]][chosen[0]+dx[cc]]
                if cellCheck == 0:
                    cellList.append((chosen[0]+dx[cc],chosen[1]+dy[cc]))
                cc+=1
            cellList.pop(chosenID)

    return extraMaze(maze),startpos,endpos


def padMaze(maze,size):
    #duct-taped function written by sam0s
    f=maze
    size=size
    ff=[]
    for numb in range(size+2):
        ff.append([-1]*(size+2))
    x=0
    y=1
    for numb in range(size):
        for a in ff[y][:-2]:
            x+=1
            ff[y][x]=f[y-2][x-2]
        x=0
        y+=1
    return ff

def extraMaze(maze):
    #place crates
    xx=0
    yy=0

    for x in maze:
        for y in x:
            if y==-1:
                maze[yy][xx]=0
            if y==1:
                maze[yy][xx]=random.choice([3,4,4,4]+[1]*89)
            xx+=1
        yy+=1
        xx=0
    return maze
