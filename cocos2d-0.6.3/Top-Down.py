from cocos.director import *
from cocos.scene import *
from cocos.layer import *
from cocos.sprite import *
from cocos.actions import *
from cocos.tiles import *
import cocos
import math

LEFT = 65361
RIGHT = 65363
UP = 65362
DOWN = 65364
SPACE = 32
A = 97
D = 100
W = 119
S = 115

one_eighty_over_pi = 57.2957795131

class GameLayer(Layer):
    is_event_handler = True
    def __init__(self):
        super(GameLayer, self).__init__()
        self.schedule(self.update)
        self.mouse_x,self.mouse_y = 0,0
        self.player_sprite = Sprite('resources/player_sprites/player.gif',position=(400,304))
        self.add(self.player_sprite)
        self.chars_pressed = set()
        
        self.player_inventory = ["rifle","shotgun","handgun"]
        self.player_sprite.mode = "idle"
        self.index = 0
        self.player_sprite.weapon = self.player_inventory[self.index]
    def update(self,dt):
        #gameloop
        
        
        #
        ##
        ### show the right sprite for movement
         
        
        
        ### show the right sprite for movement
        ##
        #
        
        
        
        #
        ##
        ### point player towards mouse
        self.player_vector = [self.mouse_x-self.player_sprite.x,self.mouse_y-self.player_sprite.y]
        self.angle = math.atan2(*self.player_vector)
        self.angle *= one_eighty_over_pi
        self.player_sprite.do(RotateTo(self.angle-95,0))
         ### point player towards mouse
         ##
         #
         
         
         
         #
         ##
         ### move player
        x,y = self.player_sprite.position
        
        if W in self.chars_pressed:
            y += 5
        if A in self.chars_pressed:
            x -= 5
        if S in self.chars_pressed:
            y -= 5
       
        if D in self.chars_pressed:
            x += 5
        self.player_sprite.position = x,y
        ### move player
        ##
        #
        
        
        
        
        
       
        
        
       
       
       
    def on_mouse_motion(self,x,y,dx,dy):
        self.mouse_x,self.mouse_y = x,y
    def on_key_press(self,key,modifiers):
        self.chars_pressed.add(key)
        
        
    def on_key_release(self,key,modifiers):
        self.chars_pressed.remove(key)
        


if __name__ == "__main__":
    director.init(width=800,height=608)
    game_scene = Scene(GameLayer())
    director.run(game_scene)