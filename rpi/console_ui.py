import os
import time
from rich import print
from rich.markdown import Markdown
from rich.panel import Panel
from rich.columns import Columns
from rich.bar import Bar

title = Panel("[blue]Smart Hallway Lighting", title="[grey74]IoT Project[/grey74]",subtitle="[grey35]David Grawe, Yizhou Yang" ,expand=True)
title.border_style = "grey35"
title.subtitle_align = "right"
title.padding= (1,4)

def print_data(mode = "", sensor = 0.5, domain = "", lights = [], threads = ""):
	os.system('cls' if os.name == 'nt' else 'clear')
	print(title)
	print(Columns([
		Panel(mode, title="Mode"),
		Panel(domain,style = "grey35" , title="Domain"),
		Panel(f"Value: {sensor}", title="Sensor"),
		Panel(threads, style= "grey35", title = "Threads")], expand=True),
		Panel(Bar(1,sensor-0.01,sensor+0.01), title="Sensor"))
	#l = []
	for i in lights:
		if i.on:
			print(Bar(i.max, i.position-i.radius, i.position+i.radius))
	#print(Panel(l,border_style="grey74" , title="Lights"))
	print("Enter 'exit' to exit, enter 'on', 'off' or 'auto' to change mode or enter a float to change sensor value while debugging:")
