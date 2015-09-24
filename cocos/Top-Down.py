from cocos.director import *
from cocos.scene import *
from cocos.layer import *
from cocos.sprite import *
from cocos.actions import *
import cocos.tiles
import cocos.text

import cocos.collision_model as cm

import cocos
import math
import numpy
from heapq import *



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

ONE = 49
TWO = 50
THREE = 51
FOUR = 52
FIVE = 53

one_eighty_over_pi = 57.2957795131

### Declaring some global variables that will be very useful later
##
#




class Enemy(object):
    def __init__(self,x,y):
        self.health = 3
        self.x = x
        self.y = y
        self.img = Sprite('resources/player_sprites/zombie.png',position = (self.x,self.y))
        
        
        
        
        

class Slot(object):
    def __init__(self,position,selected):
        self.selected = selected
        self.position = position
        if self.selected:
            self.img = Sprite("resources/UI/slot2.png",position=position)
        else:
            self.img = Sprite("resources/UI/slot1.png",position=position)
        self.item = None
    def update(self):
        if self.selected:
            self.img = Sprite("resources/UI/slot2.png",position=self.position)
        else:
            self.img = Sprite("resources/UI/slot1.png",position=self.position)
    
    
        
        
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
        
        self.map = cocos.tiles.load('lvl1.tmx')['1']
        self.scroller.add(self.map,-1,'test')
        
        
        
        ### Load Map
        ##
        #
        
        #
        ##
        ### Inventory/HUD
        
        self.hud_layer = cocos.layer.ColorLayer(255, 0, 0, 255, width=100, height=2)     
        self.hud_layer.opacity = 100   
        game_scene.add(self.hud_layer,z=1)
        
       
        self.slots = {
            1:Slot(position=(736,456),selected=True),
            2:Slot(position=(736,392),selected=False),
            3:Slot(position=(736,328),selected=False),
            4:Slot(position=(736,264),selected=False),
            5:Slot(position=(736,200),selected=False)
        }
        
        for slot in self.slots:
            self.hud_layer.add(self.slots[slot].img)
        
        
    
        self.round = 1
        self.round_label = cocos.text.Label(text='%s' % self.round,position=(36,130),font_size=15)
        self.hud_layer.add(self.round_label)
        
        
        ### Inventory/HUD
        ##
        #
        
        #
        ##
        ### Player 
        
        self.player_sprite = Sprite('resources/player_sprites/player.png',position=(200,240))
        self.add(self.player_sprite)
        self.chars_pressed = set()
        
        
        
        self.magazine = 30
        self.ammo = 120
        
        self.rifle = Sprite("resources/weapon_sprites/rifle.png")
        self.player_sprite.add(self.rifle)
        
        ###
        ##
        #
        
        
        #
        ##
        ### Collision
        
        
        self.collision_manager = cm.CollisionManagerBruteForce()
        self.player_sprite.cshape = cm.AARectShape(
            self.player_sprite.position,
            self.player_sprite.width//2,
            self.player_sprite.height//2
        )
        self.collision_manager.add(self.player_sprite)
        
        ### Collision
        ##
        #
        
        
        #
        ##
        ### Setting up enemy batch
        
        self.batch = cocos.batch.BatchNode()
        self.add(self.batch,z=1)
        
        ### Setting up enemy batch
        ##
        #
        
        
        
        
        
        
        
    
        
        
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
            y += 4
        if A in self.chars_pressed:
            x -= 4
        if S in self.chars_pressed:
            y -= 4
        if D in self.chars_pressed:
            x += 4
    
      
        
        
        
        self.player_sprite.position = x,y
        
        
        
        self.scroller.set_focus(x,y)
        self.set_view(x, y, x+800, y+608, viewport_ox=400, viewport_oy=304)
        self.scroller.get('test').set_view(0, 0, 800, 800, -x, -y)
             
        ### move player
        ##
        #
        
        
        #
        ##
        ### inventory 
        
        for i in self.slots:
            self.hud_layer.remove(self.slots[i].img)
        
        if ONE  in self.chars_pressed:
            for i in self.slots:
                self.slots[i].selected = False
            self.slots[1].selected = True
            for i in self.slots:
                self.slots[i].update()
        if TWO  in self.chars_pressed:
            for i in self.slots:
                self.slots[i].selected = False
            self.slots[2].selected = True
            for i in self.slots:
                self.slots[i].update()
        if THREE  in self.chars_pressed:
            for i in self.slots:
                self.slots[i].selected = False
            self.slots[3].selected = True
            for i in self.slots:
                self.slots[i].update()
        if FOUR  in self.chars_pressed:
            for i in self.slots:
                self.slots[i].selected = False
            self.slots[4].selected = True
            for i in self.slots:
                self.slots[i].update()
        if FIVE  in self.chars_pressed:
            for i in self.slots:
                self.slots[i].selected = False
            self.slots[5].selected = True
            for i in self.slots:
                self.slots[i].update()
       
        
        for i in self.slots:
            if self.slots[i].img not in self.hud_layer:
                self.hud_layer.add(self.slots[i].img)
        
        ### inventory
        ##
        #
        
        
       
        
        
       
       
    def on_mouse_press (self, x, y, buttons, modifiers):
        self.fire()
        
    def on_mouse_motion(self,x,y,dx,dy):
        self.mouse_x,self.mouse_y = director.get_virtual_coordinates(x, y)

    def on_mouse_drag (self, x, y, dx, dy, buttons, modifiers):
        self.mouse_x,self.mouse_y = x,y       
    def on_key_press(self,key,modifiers):
        self.chars_pressed.add(key)
    def on_key_release(self,key,modifiers):
        self.chars_pressed.remove(key)
    def fire(self):
        pass
        
        


        


if __name__ == "__main__":
    director.init(width=800,height=608,caption="Top-Down")
    game_scene = Scene()
    game_scene.add(GameLayer())
    director.run(game_scene)