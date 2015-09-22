from pyglet import *
from pyglet.window import key
from pyglet.window import mouse

#800x608 = 25x19 in 32x32 tiles


class Window(window.Window):
    def __init__(self):
        super(Window,self).__init__()
        
       # self.t0 = resource.image('0.png')
                
        self.set_size(608,608)
       # self.set_icon(self.t0,self.t0)
    def on_draw(self):
        self.clear()
        graphics.draw_indexed(3,gl.GL_TRIANGLES,[0,1,2],('v2i',(300,350,250,250,350,250 )) ) 
        
        
        
        
        
if __name__ == "__main__" :  
    window = Window()
    app.run()





