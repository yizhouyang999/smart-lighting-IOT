lights = []
comfort = 0.05

class Light():
    def __init__(self, id, position, radius, on = False) -> None:
        self.id = id
        self.position = position
        self.radius = radius
        self.on = on
        
    def isOn(self) -> bool:
        """Returns True if the light is on, False otherwise."""
        return self.on

    def turn(self, state:str) -> None:
        """Turns the light On or Off. Accepts "On" or "Off" as arguments."""
        # make shure state is "On" or "Off"
        if state not in ["On", "Off"]:
            raise ValueError("state must be either On or Off")
        else:
            self.on = state == "On"
        
    def illuminate(self, pos:float) -> None:
        global comfort
        p = self.position
        r = self.radius
        c = comfort
        should_be_on = p - r < pos + c and pos - c < p + r
        self.turn("On" if should_be_on else "Off")

# generates all lights from the lights.txt file and puts them in the lights list
with open("lights.txt") as f:
    for line in f:
        if line[0] in ["#", "\n"]:
            continue
        try:
            id, position, radius = line.split()
            lights.append(Light(id, float(radius), float(position)))
        except:
            pass

def getLightsState() -> None:
    return
