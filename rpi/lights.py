# initialize the list of lights and the illuminated area
lights = []
area = (1, 3)

# define a Light class to represent each light
class Light:
    def __init__(self, radius, position, area):
        self.radius = radius
        self.position = position
        self.area = area
        self.is_on = False

# define a function to toggle the lights on or off
def toggle_lights():
    for light in lights:
        # if the light's area intersects the illuminated area, toggle its state
        if light.position + light.radius > area[0] and light.position - light.radius < area[1]:
            light.is_on = not light.is_on

# create some lights and add them to the list
lights.append(Light(1, 2, (1, 3)))
lights.append(Light(2, 4, (2, 5)))
lights.append(Light(3, 6, (3, 6)))

# toggle the lights on or off
toggle_lights()
