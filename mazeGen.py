# Random Maze Generator using Depth-first Search
# http://en.wikipedia.org/wiki/Maze_generation_algorithm
# FB36 - 20130106
#Ruined by sam0s
import random

def padMaze(maze,size):
    #duct-taped function written by sam0s
    f=maze
    size=size
    ff=[]
    for numb in range(size+2):
        ff.append([0]*(size+2))
    x=0
    y=1
    for numb in range(size):
        for a in ff[y][:-2]:
            x+=1
            ff[y][x]=f[y-2][x-2]
        x=0
        y+=1
    return ff

def generate(size):
    mx = size; my = size # width and height of the maze
    maze = [[0 for x in range(mx)] for y in range(my)]
    dx = [0, 1, 0, -1]; dy = [-1, 0, 1, 0] # 4 directions to move in the maze
    # start the maze from a random cel
    cx = random.randint(0, mx - 1); cy = random.randint(0, my - 1)
    maze[cy][cx] = 1; stack = [(cx, cy, 0)] # stack element: (x, y, direction)

    while len(stack) > 0:
        (cx, cy, cd) = stack[-1]
        # to prevent zigzags:
        # if changed direction in the last move then cannot change again
        if len(stack) > 2:
            if cd != stack[-2][2]: dirRange = [cd]
            else: dirRange = range(4)
        else: dirRange = range(4)

        # find a new cell to add
        nlst = [] # list of available neighbors
        for i in dirRange:
            nx = cx + dx[i]; ny = cy + dy[i]
            if nx >= 0 and nx < mx and ny >= 0 and ny < my:
                if maze[ny][nx] == 0:
                    ctr = 0 # of occupied neighbors must be 1
                    for j in range(4):
                        ex = nx + dx[j]; ey = ny + dy[j]
                        if ex >= 0 and ex < mx and ey >= 0 and ey < my:
                            if maze[ey][ex] == 1: ctr += 1
                    if ctr == 1: nlst.append(i)

        # if 1 or more neighbors available then randomly select one and move
        if len(nlst) > 0:
            ir = nlst[random.randint(0, len(nlst) - 1)]
            cx += dx[ir]; cy += dy[ir]; maze[cy][cx] = 1
            stack.append((cx, cy, ir))
        else: stack.pop()

    #duct-taped maze mods
    maze=padMaze(maze,size)
    startpos=(0,0)
    endpos=(0,0)


    #place starting pos
    while startpos==(0,0):
        xx=0
        yy=0
        for x in maze:
            for y in x:
                if y==1:
                    if random.choice([True]+[False]*700):startpos=(xx,yy)
                xx+=1
            yy+=1
            xx=0

    #place crates
    xx=0
    yy=0

    for x in maze:
        for y in x:
            if y==1:
                maze[yy][xx]=random.choice([3,4,4,4]+[1]*89)
            xx+=1
        yy+=1
        xx=0

    return (maze,startpos,endpos)
