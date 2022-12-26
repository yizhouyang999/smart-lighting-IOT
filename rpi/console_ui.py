import os
import time
from rich import print
from rich.markdown import Markdown
from rich.panel import Panel
from rich.columns import Columns
from rich.bar import Bar
from rich.console import Group

title = Panel("[blue]Smart Hallway Lighting", title="[grey74]IoT Project[/grey74]",subtitle="[grey35]David Grawe, Yizhou Yang" ,expand=True)
title.border_style = "grey35"
title.subtitle_align = "right"
title.padding= (1,4)

def print_data(mode = "", sensor = 0.5, domain = "", lights = [], threads = ""):
	m = Panel(mode, title="Mode")
	d = Panel(domain,style = "grey35" , title="Domain")
	s = Panel(f"Value: {sensor}", title="Sensor")
	t = Panel(threads, style= "grey35", title = "Threads")
	os.system('cls' if os.name == 'nt' else 'clear')
	print(title)
	print(Columns([m, d, s, t], expand=True))
	print(Panel(Group(Bar(1,sensor-0.01,sensor+0.01), Bar(1, sensor-0.05, sensor+0.05, color="grey35")), title="Sensor", expand=True))
	g = Group()
	l = ""
	for i in lights:
		g.renderables.append(Bar(1, i.position-i.radius, i.position+i.radius, color="gold1" if i.on else "grey35"))
		if i.on:
			l += f"{i.id}: {i.position} \t"
	print(Panel(g,border_style="grey74" , title="Lights", subtitle=l, subtitle_align="left", style="grey74"))
	print("Enter 'exit' to exit, enter 'on', 'off' or 'auto' to change mode or enter a float to change sensor value while debugging:")
