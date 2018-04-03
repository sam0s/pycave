from pyglet.gl import *
import assets.game as game

if __name__ == '__main__':
    window = game.Window(width=854,height=480,caption='3d Dungeon',resizable=True)
    glClearColor(0.5,0.7,1,1)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_BLEND);
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
    #glEnable(GL_CULL_FACE)
    pyglet.app.run()
