import pyglet

joysticks = pyglet.input.get_joysticks()
if joysticks:
    joystick = joysticks[0]
joystick.open()

def on_joyhat_motion(joystick, hat_x, hat_y):
    print hat_x,hat_y