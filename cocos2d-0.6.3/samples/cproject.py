from cocos.director import *
from cocos.scene import *
from cocos.layer import *
from cocos.sprite import *
from cocos.actions import *
from cocos.tiles import *
import cocos

LEFT = 65361
RIGHT = 65363
UP = 65362
DOWN = 65364
SPACE = 32
A = 97
D = 100

class MenuLayer(Layer):
    is_event_handler = True
    def __init__(self):
        super(MenuLayer, self).__init__()  
        self.player = Sprite('doge.gif',position=(320,240))
        
        
        
        
        self.player.velocity = [0,0]
        self.player.speed = 150
        self.rot = RotateBy(-10,duration=0)
        self.add(self.player,z=2)# default z is 0, this is layer 
        
        self.bg = Sprite('Bimg.png',position = (400,304))
        self.add(self.bg)
        
        
        self.chars_pressed = set()
        self.schedule(self.update)
        
        self.batch = cocos.batch.BatchNode()
        self.enemies = [Sprite('enemy.png') for i in range(6)]
        
        positions = ((250, 125), (550, 125),
                     (300, 325), (500, 325),
                     (150, 475), (650, 475))
        for num, enem in enumerate(self.enemies):
            enem.position = positions[num]
            self.batch.add(enem)
        self.add(self.batch,z=1)
        
        
   
        
   
        
    def on_key_press(self,key,modifiers):
        self.chars_pressed.add(key)
        
        
    def on_key_release(self,key,modifiers):
        self.chars_pressed.remove(key)
        
    def update(self,dt):
        x,y = self.player.position
        
        if LEFT in self.chars_pressed:  
             x -= 10
        if UP in self.chars_pressed:  
             y += 10
        if RIGHT in self.chars_pressed:  
             x += 10
        if DOWN in self.chars_pressed:  
             y -= 10
        if A in self.chars_pressed:
            self.player.do(self.rot)
        if D in self.chars_pressed:
            self.player.do(Reverse(self.rot))
        self.player.position = x,y
        


if __name__ == "__main__":     
    director.init(width=800,height=608)
    game_scene = Scene(MenuLayer())
    director.run(game_scene)

        
