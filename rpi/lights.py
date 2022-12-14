import os

# configure according to the hallway and comfort. 
# 0 means only light the person directly, 
# 1 means light the whole hallway when a person is detected
comfort = 0.05

lights = []
class Light:
    def __init__(self, id, position, radius, on = "off") -> None:
        '''Initiates a light with id, position and radius'''
        self.id = id
        self.radius = radius
        self.position = position
        self.on = on
    
    def isOn(self) -> str:
        '''Returns "on" if light is on, "off" if light is off'''
        return self.on

    def turn(self, state:str) -> None:
        '''Turns the light on or off'''
        if state == self.on:
                       return
        self.on = state
        os.popen(f"tdtool --{state} {self.id}")
       
    def illuminate(self, pos:float) -> None:
        '''Turns the light on or off depending on the position of the person'''
        global comfort
        p = self.position
        r = self.radius
        c = comfort
        should_be_on = p - r < pos + c and pos - c < p + r
        s = "on" if should_be_on else "off"
        self.turn(s)

with open("lights.txt") as f:
    for line in f:
        if line[0] in ["#","\n"]:
            continue
        try:
            id, r, p = line.split()
            # Turn off all lights
            os.popen(f"tdtool --off {id}")

            lights.append(Light(id, float(p), float(r)))
        except:
            pass