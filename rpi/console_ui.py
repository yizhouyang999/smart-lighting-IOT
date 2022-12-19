import os
import time
from rich import print
from rich.markdown import Markdown
from rich.panel import Panel
from rich.columns import Columns
from rich.bar import Bar

lines = []
title = Panel("[blue]Smart Hallway Lighting", title="[grey74]IoT Project[/grey74]",subtitle="[grey35]David Grawe, Yizhou Yang" ,expand=True)
title.border_style = "grey35"
title.subtitle_align = "right"
title.padding= (1,4)

def print_data(mode = "", sensor = 0.5, domain = "", lights = "", threads = ""):
	os.system('cls' if os.name == 'nt' else 'clear')
	print(title)
	print(Columns([
		Panel(mode, title="Mode"),
		Panel(domain,style = "grey35" , title="Domain"),
		Panel(f"Value: {sensor}", title="Sensor"),
		Panel(threads, style= "grey35", title = "Threads")], expand=True),
		Panel(Bar(1,sensor-0.01,sensor+0.01), title="Sensor"))
	print(Panel(lights,border_style="grey74" , title="Lights"))
	for line in lines:
		print(line)
def lines_add(x):
	lines.append(x)
	print_data()
