from cocos.director import *
from cocos.scene import *
from cocos.layer import *
from cocos.sprite import *
from cocos.actions import *
import cocos.tiles

import cocos
import math


#
##
### Declaring some global variables that will be very useful later
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

### Declaring some global variables that will be very useful later
##
#

class GameLayer(ScrollableLayer):
    is_event_handler = True
    def __init__(self):
        super(GameLayer, self).__init__()
        self.schedule(self.update)
        self.mouse_x,self.mouse_y = 0,0
        
        #
        ##
        ### Load Map
        self.scroller = ScrollingManager()
        self.add(self.scroller,z=-1)
        
        self.map = cocos.tiles.load('resources/map.tmx')['1']
        self.scroller.add(self.map,0,'test')
        
        
        ### Load Map
        ##
        #
        
        #self.view_w = 800
        #self.view_h = 608
        
        
        
        
        
        self.player_sprite = Sprite('resources/player_sprites/player.gif',position=(400,304))
        self.add(self.player_sprite)
        self.chars_pressed = set()
        
        
        self.weapon_inventory = ["rifle","shotgun","handgun"]
        self.weapon_capacities = {
            "rifle":30,
            "shotgun":8,
            "handgun":15
        }
        self.ammo = {
            "rifle":120,
            "shotgun":16,
            "handgun":45
        }
        
        self.magazines = {
            "rifle":30,
            "shotgun":8,
            "handgun":15
        }
        
        self.index = 0
        self.player_sprite.weapon = self.weapon_inventory[self.index]
       
        
        
        
        
        
    
        
        
    def update(self,dt):
        
        #gameloop
        
        x = self.player_sprite.position[0]
        y = self.player_sprite.position[1]
        
        
        #
        ##
        ### show the right sprite for movement
        
        
        
        ### show the right sprite for movement
        ##
        #
        
        
        
        #
        ##
        ### point player towards mouse
        self.player_vector = [self.mouse_x-400,self.mouse_y-304]
        self.angle = math.atan2(*self.player_vector)
        self.angle *= one_eighty_over_pi
        self.player_sprite.do(RotateTo(self.angle-95,0))
        ### point player towards mouse
        ##
        #
         
         
         
        #
        ##
        ### move player
        
        
        if W in self.chars_pressed:
            y += 5
        if A in self.chars_pressed:
            x -= 5
        if S in self.chars_pressed:
            y -= 5
        if D in self.chars_pressed:
            x += 5
        self.player_sprite.position = x,y
        
        self.scroller.set_focus(x,y)
        self.set_view(x, y, x+800, y+608, viewport_ox=400, viewport_oy=304)
        self.scroller.get('test').set_view(0, 0, 800, 800, -x, -y)
             
        ### move player
        ##
        #
        
        
        
        
        
       
        
        
       
       
    def on_mouse_press (self, x, y, buttons, modifiers):
        if self.index < 1:
            self.fire("auto")
        else:
            self.fire("semi")
        
    def on_mouse_motion(self,x,y,dx,dy):
        self.mouse_x,self.mouse_y = director.get_virtual_coordinates(x, y)
        
    def on_key_press(self,key,modifiers):
        self.chars_pressed.add(key)
    def on_key_release(self,key,modifiers):
        self.chars_pressed.remove(key)
    def fire(self,mode):
        if mode == "auto":
            pass
        elif mode == "semi":
            pass
        


        


if __name__ == "__main__":
    director.init(width=800,height=608,caption="Top-Down")
    game_scene = Scene(GameLayer())
    director.run(game_scene)