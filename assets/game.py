from pyglet.gl import *
from pyglet.window import key
import math
import assets.mazeGen as mazeGen
from os import path

def distance(s,e):
    #should be set of 3 numbers per position
    #returns distance between two points
    s=[s[0],s[2]]
    e=[e[0],e[2]]
    total = math.sqrt((s[0] - e[0])**2 + (s[1] - e[1])**2)
    return total

def get_tex(file):
    tex = pyglet.image.load(file).texture
    glTexParameterf(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT);
    return pyglet.graphics.TextureGroup(tex)

FLAT_TEXTURE_GROUP={
'floor':get_tex(path.join('images','floor.png')),
'wall':get_tex(path.join('images','wall.png')),
'ceiling':get_tex(path.join('images','ceiling.png')),
'chestside':get_tex(path.join('images','chests.png')),
'chesttop':get_tex(path.join('images','chestt.png')),
'enemy1':get_tex(path.join('images','orc.png'))
}

class Model:
    def __init__(self):
        self.top=0
        self.bottom=0
        self.side=0
        self.batch = pyglet.graphics.Batch()

        self.extras=[]
        self.enemies=[]
        self.batch2 = pyglet.graphics.Batch()

    def add_wall(self,sx,sy,sz,tex):
        tex_coords = ('t2f',(0,0, 1,0, 1,1, 0,1))
        x,y,z = sx,sy,sz
        X,Y,Z = x+1,y+1,z+1

        self.batch.add(4,GL_QUADS,FLAT_TEXTURE_GROUP['wall'],('v3f',(x,y,z, x,y,Z, x,Y,Z, x,Y,z, )),tex_coords)
        self.batch.add(4,GL_QUADS,FLAT_TEXTURE_GROUP['wall'],('v3f',(X,y,Z, X,y,z, X,Y,z, X,Y,Z, )),tex_coords)
        self.batch.add(4,GL_QUADS,FLAT_TEXTURE_GROUP['wall'],('v3f',(x,y,z, X,y,z, X,y,Z, x,y,Z, )),tex_coords)
        self.batch.add(4,GL_QUADS,FLAT_TEXTURE_GROUP['wall'],('v3f',(x,Y,Z, X,Y,Z, X,Y,z, x,Y,z, )),tex_coords)
        self.batch.add(4,GL_QUADS,FLAT_TEXTURE_GROUP['wall'],('v3f',(X,y,z, x,y,z, x,Y,z, X,Y,z, )),tex_coords)
        self.batch.add(4,GL_QUADS,FLAT_TEXTURE_GROUP['wall'],('v3f',(x,y,Z, X,y,Z, X,Y,Z, x,Y,Z, )),tex_coords)

    def create_room(self):
        tex_coords = ('t2f',(0,0, 16,0, 16,16, 0,16, ))
        self.batch.add(4,GL_QUADS,FLAT_TEXTURE_GROUP['floor'],('v3f',(0,0,0, 0,0,27, 27,0,27, 27,0,0) ),tex_coords)

    def draw(self):
        self.batch.draw()
        self.batch2.draw()

        for f in self.enemies:
            for face in f.geometry:
                try:
                    face.delete()
                    f.geometry=[]
                except:
                    pass


#key/direction matrix (says how we should move based on where we are looking and what key we press)
KDM={'w':{'n':(0,1),'e':(-1,0),'s':(0,-1),'w':(1,0),},
    's':{'n':(0,-1),'e':(1,0),'s':(0,1),'w':(-1,0),},
    'a':{'n':(1,0),'e':(0,1),'s':(-1,0),'w':(0,-1),},
    'd':{'n':(-1,0),'e':(0,-1),'s':(1,0),'w':(0,1),}}


class Crate:
    def __init__(self,pos=(0,0,0),batch=None):
        self.pos=list(pos)
        self.geometry=[]
        self.batch=batch
        self.wid=(self.pos[0],self.pos[2])

        sx=self.pos[0]+0.4
        sy=0
        sz=self.pos[2]+0.4

        tex_coords = ('t2f',(0,0, 1,0, 1,1, 0,1))
        x,y,z = sx,sy,sz
        X,Y,Z = x+0.2,y+0.2,z+0.2

        self.geometry.append(self.batch.add(4,GL_QUADS,FLAT_TEXTURE_GROUP['chestside'],('v3f',(x,y,z, x,y,Z, x,Y,Z, x,Y,z, )),tex_coords))#front
        self.geometry.append(self.batch.add(4,GL_QUADS,FLAT_TEXTURE_GROUP['chestside'],('v3f',(X,y,Z, X,y,z, X,Y,z, X,Y,Z, )),tex_coords))#back
        self.geometry.append(self.batch.add(4,GL_QUADS,FLAT_TEXTURE_GROUP['chestside'],('v3f',(x,y,z, X,y,z, X,y,Z, x,y,Z, )),tex_coords))#bottom
        self.geometry.append(self.batch.add(4,GL_QUADS,FLAT_TEXTURE_GROUP['chesttop'],('v3f',(x,Y,Z, X,Y,Z, X,Y,z, x,Y,z, )),tex_coords))#top
        self.geometry.append(self.batch.add(4,GL_QUADS,FLAT_TEXTURE_GROUP['chestside'],('v3f',(X,y,z, x,y,z, x,Y,z, X,Y,z, )),tex_coords))#left
        self.geometry.append(self.batch.add(4,GL_QUADS,FLAT_TEXTURE_GROUP['chestside'],('v3f',(x,y,Z, X,y,Z, X,Y,Z, x,Y,Z, )),tex_coords))#right

    def update(self):
        pass

class Enemy:
    def __init__(self,pos=(0,0,0),mod=None,pref=None):
        self.pos=list(pos)
        self.geometry=[]
        self.batch=mod.batch2
        self.pref=pref
        self.wid=(self.pos[0],self.pos[2])

        sx=self.pos[0]-0.4
        sy=0
        sz=self.pos[2]+0.1

        tex_coords = ('t2f',(0,0, 1,0, 1,1, 0,1))
        x,y,z = sx,sy,sz
        X,Y,Z = x+0.8,y+0.8,z+0.8

        self.geometry.append(self.batch.add(4,GL_QUADS,FLAT_TEXTURE_GROUP['enemy1'],('v3f',(X,y,Z, X,y,z, X,Y,z, X,Y,Z, )),tex_coords))
        self.rota=1
    def update(self):
        self.rota=1
        sx=self.pos[0]-0.5
        sz=self.pos[2]
        sy=0
        if self.pref.pos[0]<self.pos[0] and self.pos[2]==math.floor(self.pref.pos[2]):
            self.rota=3
            sx=self.pos[0]+0.5
        if self.pref.pos[0]>self.pos[0] and self.pos[2]==math.floor(self.pref.pos[2]):
            self.rota=1
            sx=self.pos[0]-0.5
            sz=self.pos[2]
        if self.pref.pos[2]<self.pos[2] and self.pos[0]==math.floor(self.pref.pos[0]):
            self.rota=4
            sz=self.pos[2]+0.5
            sx=self.pos[0]
        if self.pref.pos[2]>self.pos[2] and self.pos[0]==math.floor(self.pref.pos[0]):
            self.rota=2
            sz=self.pos[2]-0.5
            sx=self.pos[0]

        tex_coords = ('t2f',(0,0, 1,0, 1,1, 0,1))
        x,y,z = sx,sy,sz
        X,Y,Z = x+0.8,y+0.8,z+0.8

        if self.rota==1:
            self.geometry.append(self.batch.add(4,GL_QUADS,FLAT_TEXTURE_GROUP['enemy1'],('v3f',(X,y,Z, X,y,z, X,Y,z, X,Y,Z, )),tex_coords))
        if self.rota==2:
            self.geometry.append(self.batch.add(4,GL_QUADS,FLAT_TEXTURE_GROUP['enemy1'],('v3f',(x,y,Z, X,y,Z, X,Y,Z, x,Y,Z, )),tex_coords))
        if self.rota==3:
            self.geometry.append(self.batch.add(4,GL_QUADS,FLAT_TEXTURE_GROUP['enemy1'],('v3f',(x,y,z, x,y,Z, x,Y,Z, x,Y,z, )),tex_coords))
        if self.rota==4:
            self.geometry.append(self.batch.add(4,GL_QUADS,FLAT_TEXTURE_GROUP['enemy1'],('v3f',(X,y,z, x,y,z, x,Y,z, X,Y,z, )),tex_coords))

class Player:
    def __init__(self,pos=(0,0,0),rot=(0,0),world=[],mod=None):
        self.pos = list(pos)
        self.rot = list(rot)
        self.bobFrame=0
        self.target=0
        self.world=world
        self.ms=0.02
        self.model=mod
    def mouse_motion(self,dx,dy):
        dx/=8; dy/=8; self.rot[0]+=dy; self.rot[1]-=dx
        if self.rot[0]>90: self.rot[0] = 90
        elif self.rot[0]<-90: self.rot[0] = -90
    def get_facing(self,rot):
        rot=round(rot)
        dAngs={'n':(135,225),'e':(226,315),'s1':(316,360),'s2':(0,45),'w':(46,134)}
        if rot>=dAngs['n'][0] and rot<=dAngs['n'][1]: return 'n'
        if rot>=dAngs['e'][0] and rot<=dAngs['e'][1]: return 'e'
        if rot>=dAngs['s1'][0] and rot<=dAngs['s1'][1]: return 's'
        if rot>=dAngs['s2'][0] and rot<=dAngs['s2'][1]: return 's'
        if rot>=dAngs['w'][0] and rot<=dAngs['w'][1]: return 'w'
    def update(self,dt,keys):
        #update camera bob
        if self.bobFrame>=3.1:self.bobFrame=0
        self.pos[1]=(0.5+abs(math.sin(self.bobFrame))/22)
        #speed
        s = dt*100
        a=1
        #Find the current coterminal of the facing angle in degrees
        rotY = -self.rot[1]/180*math.pi
        rotdeg=rotY*180/math.pi
        while rotdeg>360:
            rotdeg-=360
        while rotdeg<0:
            rotdeg+=360
        #facing direction
        fd=self.get_facing(rotdeg)
        if keys[key.SPACE]:self.pos[1]+=0.1
        if self.target==0:
            if keys[key.W]: self.target=[self.pos[0]+KDM['w'][fd][0],self.pos[2]+KDM['w'][fd][1]]
            elif keys[key.S]: self.target=[self.pos[0]+KDM['s'][fd][0],self.pos[2]+KDM['s'][fd][1]]
            elif keys[key.A]: self.target=[self.pos[0]+KDM['a'][fd][0],self.pos[2]+KDM['a'][fd][1]]
            elif keys[key.D]: self.target=[self.pos[0]+KDM['d'][fd][0],self.pos[2]+KDM['d'][fd][1]]
        else:
            #grid position of player (world-x,world-y)
            wx=int(self.target[0])
            wy=int(self.target[1])

            #if collide with crate, break it.
            if self.world[wy][wx]==3:
                for extrablock in self.model.extras:
                    if extrablock.wid==(wx,wy):
                        self.model.extras.pop(self.model.extras.index(extrablock))
                        for face in extrablock.geometry:face.delete()

            if self.world[wy][wx] != 0:
                #move until we reach our target!
                #round so that we land perfectly on 0.
                self.pos[0],self.pos[2]=round(self.pos[0],2),round(self.pos[2],2)
                a=0
                if self.pos[0]<self.target[0]:
                    self.pos[0]+=self.ms*s
                    if self.pos[0]>self.target[0]:self.pos[0]=self.target[0]
                elif self.pos[0]>self.target[0]:
                    self.pos[0]-=self.ms*s
                    if self.pos[0]<self.target[0]:self.pos[0]=self.target[0]
                elif self.pos[2]<self.target[1]:
                    self.pos[2]+=self.ms*s
                    if self.pos[2]>self.target[1]:self.pos[2]=self.target[1]
                elif self.pos[2]>self.target[1]:
                    self.pos[2]-=self.ms*s
                    if self.pos[2]<self.target[1]:self.pos[2]=self.target[1]
                else: self.target=0; #perfect 0 landing
            else:self.target=0; #perfect 0 landing

        #bobit
        if a==1:
            #recovery bob
            if self.bobFrame!=0:
                self.bobFrame+=0.32
        else:
            #bob while moving
            self.bobFrame+=3 / ( (1/(self.ms*s))/2 )

class Window(pyglet.window.Window):

    def push(self,pos,rot): glPushMatrix(); glRotatef(-rot[0],1,0,0); glRotatef(-rot[1],0,1,0); glTranslatef(-pos[0],-pos[1],-pos[2],)
    def Projection(self): glMatrixMode(GL_PROJECTION); glLoadIdentity()
    def Model(self): glMatrixMode(GL_MODELVIEW); glLoadIdentity()

    def set2d(self):
        width, height = self.get_size()
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, width, 0, height, -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def set3d(self): self.Projection(); gluPerspective(70,self.width/self.height,0.05,1000); self.Model()

    def setLock(self,state): self.lock = state; self.set_exclusive_mouse(state)
    lock = False; mouse_lock = property(lambda self:self.lock,setLock)

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.set_minimum_size(300,200)
        self.keys = key.KeyStateHandler()
        self.push_handlers(self.keys)
        pyglet.clock.schedule(self.update)

        #World Model
        self.model=Model()
        self.model.create_room()

        #set up initial weapon position
        self.weaponSprite=pyglet.sprite.Sprite(pyglet.image.load(path.join('images','fork.png')).get_region(x=0,y=0,width=100,height=100))
        self.weaponSprite.scale=((self.width+self.height)/650)
        self.weaponSprite.x=(self.width // 2)-self.weaponSprite.width/2


        gameLevel,playerPos,endPos=mazeGen.generate(25)
        #self.player = Player((playerPos[0],0.3,playerPos[1]),(-30,0))
        self.player = Player((playerPos[0]+0.5,0.5,playerPos[1]+0.5),(-30,0),gameLevel,self.model)

        #build world (will move to model class soon)
        x=0
        y=0
        enemylimit=999
        for row in gameLevel:
            for col in row:
                if col==0:self.model.add_wall(x,0,y,"")
                if col==3:self.model.extras.append(Crate((x,0,y),self.model.batch))
                if col==4:
                    if enemylimit>0:self.model.enemies.append(Enemy((x,0,y),self.model,self.player));enemylimit-=1
                x+=1
            x=0
            y+=1

        #reticle setup
        x, y = self.width // 2, self.height // 2
        n = 10
        self.reticle = pyglet.graphics.vertex_list(4,
            ('v2i', (x - n, y, x + n, y, x, y - n, x, y + n))
        )


    def on_resize(self, width, height):
        #weaponSprite
        self.weaponSprite.scale=((self.width+self.height)/650)
        self.weaponSprite.x=(self.width // 2)-self.weaponSprite.width/2

        # reticle
        if self.reticle:
            self.reticle.delete()
        x, y = self.width // 2, self.height // 2
        n = 10
        self.reticle = pyglet.graphics.vertex_list(4,
            ('v2i', (x - n, y, x + n, y, x, y - n, x, y + n))
        )

    def on_mouse_motion(self,x,y,dx,dy):
        #if self.reticle:self.reticle.delete() SAFE
        if self.mouse_lock: self.player.mouse_motion(dx,dy)

    def on_key_press(self,KEY,MOD):
        if KEY == key.ESCAPE: self.close()
        elif KEY == key.E: self.mouse_lock = not self.mouse_lock

    def update(self,dt):
        self.player.update(dt,self.keys)
        for enemy in self.model.enemies:
            enemy.update()

    def draw_reticle(self):
        glColor3d(0, 0, 0)
        self.reticle.draw(GL_LINES)

    def on_draw(self):
        self.clear()
        self.set3d()
        self.push(self.player.pos,self.player.rot)
        self.model.draw()
        glPopMatrix()
        self.set2d()
        self.draw_reticle()
        self.weaponSprite.draw()
        glColor3d(1,1,1)
