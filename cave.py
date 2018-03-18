from pyglet.gl import *
from pyglet.window import key
import math
import mazeGen
from os import path

def vec(*args):
    return (GLfloat * len(args))(*args)

class Model:

    def get_tex(self,file):
        tex = pyglet.image.load(file).texture
        glTexParameterf(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT);
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT);
        return pyglet.graphics.TextureGroup(tex)

    def __init__(self):
        self.top=0
        self.bottom=0
        self.side=0

        self.flatTextureGroup={
        'floor':self.get_tex(path.join('images','floor.png')),
        'wall':self.get_tex(path.join('images','wall.png')),
        'ceiling':self.get_tex(path.join('images','ceiling.png')),
        }



        self.batch = pyglet.graphics.Batch()
    def add_wall(self,sx,sy,sz,tex):
        tex_coords = ('t2f',(0,0, 1,0, 1,1, 0,1))
        x,y,z = sx,sy,sz
        X,Y,Z = x+1,y+1,z+1

        self.batch.add(4,GL_QUADS,self.flatTextureGroup['wall'],('v3f',(x,y,z, x,y,Z, x,Y,Z, x,Y,z, )),tex_coords)
        self.batch.add(4,GL_QUADS,self.flatTextureGroup['wall'],('v3f',(X,y,Z, X,y,z, X,Y,z, X,Y,Z, )),tex_coords)
        self.batch.add(4,GL_QUADS,self.flatTextureGroup['wall'],('v3f',(x,y,z, X,y,z, X,y,Z, x,y,Z, )),tex_coords)
        self.batch.add(4,GL_QUADS,self.flatTextureGroup['wall'],('v3f',(x,Y,Z, X,Y,Z, X,Y,z, x,Y,z, )),tex_coords)
        self.batch.add(4,GL_QUADS,self.flatTextureGroup['wall'],('v3f',(X,y,z, x,y,z, x,Y,z, X,Y,z, )),tex_coords)
        self.batch.add(4,GL_QUADS,self.flatTextureGroup['wall'],('v3f',(x,y,Z, X,y,Z, X,Y,Z, x,Y,Z, )),tex_coords)

    def create_room(self):
        tex_coords = ('t2f',(0,0, 16,0, 16,16, 0,16, ))
        self.batch.add(4,GL_QUADS,self.flatTextureGroup['floor'],('v3f',(0,0,0, 0,0,25, 25,0,25, 25,0,0) ),tex_coords)

    def draw(self):
        self.batch.draw()

class Player:
    def __init__(self,pos=(0,0,0),rot=(0,0)):
        self.pos = list(pos)
        self.rot = list(rot)

    def mouse_motion(self,dx,dy):
        dx/=8; dy/=8; self.rot[0]+=dy; self.rot[1]-=dx
        if self.rot[0]>90: self.rot[0] = 90
        elif self.rot[0]<-90: self.rot[0] = -90

    def update(self,dt,keys):
        s = dt*2
        rotY = -self.rot[1]/180*math.pi
        dx,dz = s*math.sin(rotY),s*math.cos(rotY)
        if keys[key.W]: self.pos[0]+=dx; self.pos[2]-=dz
        if keys[key.S]: self.pos[0]-=dx; self.pos[2]+=dz
        if keys[key.A]: self.pos[0]-=dz; self.pos[2]-=dx
        if keys[key.D]: self.pos[0]+=dz; self.pos[2]+=dx

        if keys[key.SPACE]: self.pos[1]+=s
        if keys[key.LSHIFT]: self.pos[1]-=s

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

        ###

        self.model=Model()
        self.model.create_room()

        #set up initial weapon position
        self.weaponSprite=pyglet.sprite.Sprite(pyglet.image.load(path.join('images','fork.png')).get_region(x=0,y=0,width=100,height=100))
        self.weaponSprite.scale=((self.width+self.height)/650)
        self.weaponSprite.x=(self.width // 2)-self.weaponSprite.width/2


        gameLevel,playerPos=mazeGen.generate()
        self.player = Player((playerPos[0],0.3,playerPos[1]),(-30,0))
        x=0
        y=0
        for row in gameLevel:
            for col in row:
                if col==0:self.model.add_wall(x,0,y,"")
                x+=1
            x=0
            y+=1

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
        if self.reticle:self.reticle.delete()
        if self.mouse_lock: self.player.mouse_motion(dx,dy)
        x, y = self.width // 2, self.height // 2
        n = 10
        self.reticle = pyglet.graphics.vertex_list(4,
            ('v2i', (x - n, y, x + n, y, x, y - n, x, y + n))
        )


    def on_key_press(self,KEY,MOD):
        if KEY == key.ESCAPE: self.close()
        elif KEY == key.E: self.mouse_lock = not self.mouse_lock

    def update(self,dt):
        self.player.update(dt,self.keys)

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


if __name__ == '__main__':
    window = Window(width=854,height=480,caption='3d Dungeon',resizable=True)
    glClearColor(0.5,0.7,1,1)
    glEnable(GL_DEPTH_TEST)
    #glEnable(GL_CULL_FACE)
    #setup_fog()
    pyglet.app.run()
