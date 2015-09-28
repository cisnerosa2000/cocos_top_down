from cocos.director import *
from cocos.scene import *
from cocos.layer import *
from cocos.sprite import *
from cocos.actions import *
from cocos.particle_systems import *
from cocos import shader

import cocos.tiles
import cocos.text

import cocos.collision_model as cm

import cocos
import math
import numpy
from heapq import *

import random
import inspect
from multiprocessing import Process
import subprocess



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

R = 114

ONE = 49
TWO = 50
THREE = 51
FOUR = 52
FIVE = 53

one_eighty_over_pi = 57.2957795131

### Declaring some global variables that will be very useful later



class DeathLayer(Layer):
    is_event_handler = True
    def __init__(self):
        super(DeathLayer, self).__init__()
        self.ol = cocos.text.Label(text="Game Over!",position = (400,400),font_size=30,anchor_x ='center',anchor_y='center')
        self.add(self.ol)
        
class MainMenu(cocos.menu.Menu):

    def __init__(self):
        super(MainMenu, self).__init__('Top Down')

        items = []

        items.append(cocos.menu.MenuItem('New game', self.on_new_game))
        items.append(cocos.menu.MenuItem('Options', self.on_options))
        items.append(cocos.menu.MenuItem('Quit', self.on_quit))

        self.create_menu(items)

    def on_new_game(self):
        global game_scene
        game_scene = Scene()
        game_scene.add(GameLayer())
        director.push(game_scene)
    def on_options(self):
        self.parent.switch_to(1)

    def on_quit(self):
        pyglet.app.exit()


class OptionsMenu(cocos.menu.Menu):
    def __init__(self):
        super(OptionsMenu, self).__init__('Top Down')

        items = []

        items.append(cocos.menu.ToggleMenuItem(
            'Show FPS:',
            self.on_show_fps,
            cocos.director.director.show_FPS)
        )
        items.append(cocos.menu.MenuItem('Fullscreen', self.on_fullscreen))
        items.append(cocos.menu.MenuItem('Back', self.on_quit))
        self.create_menu(items)

    def on_fullscreen(self):
        cocos.director.director.window.set_fullscreen(
            not cocos.director.director.window.fullscreen)

    def on_quit(self):
        self.parent.switch_to(0)

    def on_show_fps(self, value):
        cocos.director.director.show_FPS = value




class Enemy(object):
    def __init__(self,x,y,target):
        self.health = 3
        self.x = x
        self.y = y
        self.img = Sprite('resources/player_sprites/zombie.png',position = (self.x,self.y))
        self.img.tag = "zombie"
        target.batch.add(self.img)
        
        self.img.cshape = cm.AARectShape(
            self.img.position,
            self.img.width//2,
            self.img.height//2
        )
        target.collision_manager.add(self.img)
        
        
       
       
        
        
        
        

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
    
    
        
        
class Bullet(object):
    def __init__(self,x,y,x2,y2,target):
        self.target = target
        self.target.bullet_list.append(self)
       
        self.img = Sprite('resources/weapon_sprites/projectile.png',position=(x,y))
        self.img.tag = "bullet"
        target.bullet_batch.add(self.img)
        x,y = 400+random.randint(-15,15),304+random.randint(-15,15)
        
        self.mouse_vector = [x-x2,y-y2]
        self.c2 = self.mouse_vector[0] **2 + self.mouse_vector[1] **2
        self.c = math.sqrt(self.c2)
        self.norm = [self.mouse_vector[0]/self.c,self.mouse_vector[1]/self.c]
        self.norm[0] *= -25
        self.norm[1] *= -25
        
        self.img.cshape = cm.AARectShape(
            self.img.position,
            self.img.width//2,
            self.img.height//2
        )
        target.collision_manager.add(self.img)
        
        
        self.img.do(Repeat(MoveBy((self.norm[0],self.norm[1]),0)))
        
        

class GameLayer(ScrollableLayer):
    is_event_handler = True
    def __init__(self):
        
        super(GameLayer, self).__init__()
        self.schedule(self.update)
        self.schedule_interval(self.spawn,.2)
        self.mouse_x,self.mouse_y = 0,0
        
        director.interpreter_locals["game"] = self
                
        self.bullet_list = []
        self.enemy_list = []
        
      
        ### Load Map
        self.scroller = ScrollingManager()
        self.add(self.scroller,z=-1)
        
        self.map = cocos.tiles.load('lvl1.tmx')['1']
        self.scroller.add(self.map,-1,'test')
        
        
        ### Load Map
 
        ### Inventory/HUD
        self.max_ammo = 15
        self.magazine = self.max_ammo
        self.ammo = 30
        
        
        self.hud_layer = cocos.layer.ColorLayer(255, 0, 0, 255, width=1, height=1)    
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
        
        
        
    
        self.kills = 0
        self.kills_label = cocos.text.Label(text='%s Kills' % self.kills,position=(720,130),font_size=15,anchor_x='left')
        self.hud_layer.add(self.kills_label)
        
        self.ammo_label = cocos.text.Label(text='%s/%s' %(self.magazine,self.ammo),position=(720,100),font_size=15,anchor_x='left')
        self.health_label = cocos.text.Label(text='%d HP' %(100),position=(720,75),font_size=15,anchor_x='center')
        self.hud_layer.add(self.ammo_label)
        self.hud_layer.add(self.health_label)
        
        ### Inventory/HUD

        ### Player 
        
        self.player_sprite = Sprite('resources/player_sprites/player.png',position=(200,200))
        self.player_sprite.health = 100
        self.player_sprite.tag = "player"
        self.add(self.player_sprite)
        self.chars_pressed = set()
        
        
        
        
        self.rifle = Sprite("resources/weapon_sprites/rifle.png")
        self.player_sprite.add(self.rifle)
        self.rifle.do(MoveBy((10,4),0))
        
        
        
        ### Player

        ### Collision
        
        self.collision_manager = cm.CollisionManagerBruteForce()
        self.player_sprite.cshape = cm.AARectShape(
            self.player_sprite.position,
            self.player_sprite.width//2,
            self.player_sprite.height//2
        )
        self.collision_manager.add(self.player_sprite)
        
      
        
        ### Collision

   
        ### Setting up enemy batch
        
        self.batch = cocos.batch.BatchNode()
        self.map.add(self.batch,z=1)
        
        self.bullet_batch = cocos.batch.BatchNode()
        self.map.add(self.bullet_batch,z=1)
        
        
        ### Setting up enemy batch
        
        self.location = inspect.stack()[1][1]
        self.soundtrack()
        
        

        
        
    
        
        
    def update(self,dt):
        
        if self.player_sprite.health < 1:
            self.death()
        #gameloop
        
        x = self.player_sprite.position[0]
        y = self.player_sprite.position[1]
        
        
      
        ### Enemies / Collision
        ex,ey = self.player_sprite.x*2,self.player_sprite.y*2
        for enemy in self.enemy_list:
            try:
                vector = [ex-enemy.img.x,ey-enemy.img.x]
                angle = math.atan2(*vector)
                angle *= one_eighty_over_pi
                enemy.img.do(RotateTo(angle-95,0))
            
                pvector = [enemy.img.x-ex,enemy.img.y-ey]
                c2 = pvector[0] **2 + pvector[1] **2
                c = math.sqrt(c2)
                try:
                    enemy.norm = [pvector[0]/c,pvector[1]/c]
                    enemy.norm[0] *= -8
                    enemy.norm[1] *= -8
            
                    enemy.img.do(MoveBy((enemy.norm[0],enemy.norm[1]),0))
                except:
                    pass
                
            
                enemy.img.cshape.center = enemy.img.position
                enemy.collisions = self.collision_manager.objs_colliding(enemy.img)
                if enemy.collisions:
                    for obj in enemy.collisions:
                        if obj.tag == "zombie":
                            evec = self.away_vector(enemy.x,enemy.y,obj.x,obj.y)
                            obj.do(MoveBy((evec[0],evec[1]),0))
                        elif obj.tag == "player" and self.player_sprite.health > 0:
                            self.player_sprite.health -= 1
                    
                            
                            
                        elif obj.tag == "bullet":
                            self.kills += 1
                            self.ammo += 1 
                            
                            self.hud_layer.remove(self.kills_label)
                            self.kills_label = cocos.text.Label(text='%s Kills' % self.kills,position=(720,130),font_size=15,anchor_x='left')
                            self.hud_layer.add(self.kills_label)
                            
                            
                            try:
                                self.collision_manager.remove(obj)

                            except:
                                pass                         
                            
                            self.batch.remove(enemy.img)
                            self.enemy_list.remove(enemy)
                            self.collision_manager.remove(enemy.img)
                            del enemy
                            
                            
                            
            except:
                pass
                    
                        
                
                
                        
            
            
        
        self.player_sprite.cshape.center = (ex,ey)
        pcollisions = self.collision_manager.objs_colliding(self.player_sprite)
        
        
        
                
        
        
        ### Enemies / Collision
     
        ### bullets
        
        for b_obj in self.bullet_list:
            b_obj.dist = self.get_distance(b_obj.img.x,b_obj.img.y,self.player_sprite.x*2,self.player_sprite.y*2)
            b_obj.img.cshape.center = b_obj.img.position
            if b_obj.dist > 300:
                try:
                    self.collision_manager.remove(b_obj.img)
                    self.bullet_list.remove(b_obj)
                    self.bullet_batch.remove(b_obj.img)
                    del b_obj.img
                    del b_obj
                except:
                    pass
           
                        
           
        
        ### bullets

        ### point player towards mouse
        self.player_vector = [self.mouse_x-400,self.mouse_y-304]
        self.angle = math.atan2(*self.player_vector)
        self.angle *= one_eighty_over_pi
        self.player_sprite.do(RotateTo(self.angle-95,0))
        
        ### point player towards mouse 
 
        ### move player and handle map collision
        
        if W in self.chars_pressed:
            y += 4
        if A in self.chars_pressed:
            x -= 4
        if S in self.chars_pressed:
            y -= 4
        if D in self.chars_pressed:
            x += 4
        if R in self.chars_pressed:
            self.reload()
    
      
        self.player_sprite.position = x,y
       
        
        
        
        
        self.scroller.set_focus(x,y)
        self.set_view(x, y, x+800, y+608, viewport_ox=400, viewport_oy=304)
        self.scroller.get('test').set_view(0, 0, 800, 800, -x, -y)
             
        ### move player and handle map collision

        ### inventory 
        
        
        
        self.hud_layer.remove(self.health_label)
        self.health_label = cocos.text.Label(text='%d HP' %(self.player_sprite.health),position=(720,75),font_size=15,anchor_x='center')
        self.hud_layer.add(self.health_label)
        
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
 
     
        
        
       
        
        
       
       
    def spawn(self,dt):
        if len(self.enemy_list) < 2:
            enemy = Enemy(x=self.player_sprite.x+random.randint(-500,500),y=self.player_sprite.y+random.randint(-500,500),target=self)
            self.enemy_list.append(enemy)
    def death(self):
        death_scene = Scene()
        death_scene.add(DeathLayer())
        director.push(death_scene)
   
    def on_mouse_press (self, x, y, buttons, modifiers):
        self.fire()
    def on_mouse_release(self, x, y, buttons, modifiers):
        self.firing = False
        
    def on_mouse_motion(self,x,y,dx,dy):
        self.mouse_x,self.mouse_y = director.get_virtual_coordinates(x, y)
    
    def on_mouse_drag (self, x, y, dx, dy, buttons, modifiers):
        self.mouse_x,self.mouse_y = x,y      
    def on_key_press(self,key,modifiers):
        try:
            self.chars_pressed.add(key)
        except:
            pass
    def on_key_release(self,key,modifiers):
        try:
            self.chars_pressed.remove(key)
        except:
            pass
    def fire(self):   
        if self.magazine > 0:
            x,y = self.point_to_world((self.player_sprite.x,self.player_sprite.y))
            y,x = self.map.point_to_local((x,y))
    
            self.bullet = Bullet(x=y,y=x,x2=self.mouse_x,y2=self.mouse_y,target=self)
            self.magazine -= 1
            
            self.hud_layer.remove(self.ammo_label)
            self.ammo_label = cocos.text.Label(text='%s/%s' %(self.magazine,self.ammo),position=(700,100),font_size=15)
            self.hud_layer.add(self.ammo_label)
    def reload(self):
        n = self.max_ammo - self.magazine
        if self.ammo >= n:
            self.ammo -= n
            self.magazine += n
        else:
            self.magazine += self.ammo
            self.ammo = 0
            
            
            
        self.hud_layer.remove(self.ammo_label)
        self.ammo_label = cocos.text.Label(text='%s/%s' %(self.magazine,self.ammo),position=(700,100),font_size=15)
        self.hud_layer.add(self.ammo_label)
        
  
        
        
       
        
        


        


    def away_vector(self,startx,starty,x2,y2):
        try:
            vector = [startx-x2,starty-y2]
            c2 = vector[0] **2 + vector[1] **2
            c = math.sqrt(c2)
            norm_vector = [vector[0]/c,vector[1]/c]
        
            norm_vector[0] *= -2
            norm_vector[1] *= -2
        
            return norm_vector
        except:
            return [0,0]


    def get_distance(self,x1,y1,x2,y2):
        return math.sqrt(((x1-x2)**2)+((y1-y2)**2))
    def soundtrack(self):
        def tunes():
            if self.player_sprite.health > 0:
                cannon_audio_file = self.location.replace("Top-Down.py","soundtrack/day %s.mp3" % random.randint(1,29))
                boom = subprocess.call(["afplay", cannon_audio_file])
                tunes()
            
            
            
        self.tunesp = Process(target=tunes)
        self.tunesp.start()

if __name__ == "__main__":
    director.init(width=800,height=608,caption="Top-Down",fullscreen=False,resizable=True)
    scene = cocos.scene.Scene()
    scene.add(cocos.layer.MultiplexLayer(MainMenu(), OptionsMenu()), z=1)
    cocos.director.director.run(scene)
    
    
    
    
    
    
    
    