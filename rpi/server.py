# system libs
import sys
import time
import threading

# console and ui
from rich.panel import Panel
from rich.columns import Columns
from rich.bar import Bar
from rich.console import Group
from rich.live import Live

# own modules
import mqtt
import mode

# own modules with debug alternatives
debug = len(sys.argv)>1 and sys.argv[1] == "debug"
if debug:	import sensor_debug as 	sensor;	import lights_debug as lights
else: 		import sensor 		as	sensor;	import lights		as lights



############### UI ##################

panel_title = Panel("[blue]Smart Hallway Lighting", 
					title="[white]IoT Project[/white]",
					subtitle="[grey35]David Grawe, Yizhou Yang",
					subtitle_align="right", 
					border_style="grey35", 
					expand=True, 
					padding=(1,4))

def print_data(mode:str = "", s_value:float = -1, domain:str = "", l_list:list = [], threads:str = "") -> Group:
	'''Takes interesting data and creates a nice overview'''

	mode_text = {	"on": 	"[gold1] On [/gold1]", 
					"off": 	"[grey35] Off [/grey35]", 
					"auto": "[red] Auto [/red]"}.get(mode,mode)

	group_out = Group(
			panel_title,
			Columns([	Panel(mode_text, 		title="Mode", 		style = "grey35") ,
						Panel("[white]"+domain, title="Domain", 	style = "grey35"), 
						Panel(threads, 			title= "Threads", 	style = "grey35")
						], expand=True),
			Panel(	Group(	Bar(1, s_value-0.01, s_value+0.01), 
							Bar(1, s_value-0.05, s_value+0.05, color="grey35")), 
					title="[white]Sensor", 
					subtitle=f"[white]Value: {s_value:.2f}", 
					subtitle_align="right",
					style="grey35"))

	g = Group()
	bar_light = lambda x: Bar(1, x.position-x.radius, x.position+x.radius, color="gold1" if x.isOn() else "grey35")
	l = ""
	
	for i in l_list:
		g.renderables.append(bar_light(i))
		if i.on:
			l += f"[white]{i.id}: {i.position}[/white] ── "
	
	group_out.renderables.append(Panel(	g, 
										title="[white]Lights[/white]", 
										subtitle=l[0:-4], 
										subtitle_align="left", 
										style="grey35"))
	if debug:
		group_out.renderables.append("Enter 'exit' to exit, enter 'on', 'off' or 'auto' to change mode, enter 'r' to refresh, a number to change the sensor value or 'pong' to make the sensor value change on its own:\n")
	else:
		group_out.renderables.append("Enter 'exit' to exit, enter 'on', 'off' or 'auto' to change mode, enter anything else to refresh:\n")
	
	return group_out

# starts live preview in the console
live = Live(print_data(), auto_refresh=False, screen=True)
live.start()

def refresh(string:str = "") -> None:
	'''Function to refresh the UI'''
	global th
	if string != "":
		th = string
	live.update(print_data(m.get(), s.get(), d, l.get(), th), refresh=True)



############### Threads ##################
lock = threading.Lock()

# class to store values
class change_notifier:
	def __init__(self,data=None):
		self._data = data
	# returns True if data changed, False otherwise
	def set(self,new):
		if(self._data != new):
			self._data = new
			return True
		return False
	def get(self):
		return self._data

# set variables for threads
m = change_notifier("") 			# mode 
s = change_notifier(-1) 			# sensor value
d = "---"							# domain
l = change_notifier(lights.lights) 	# list of lights

refresh("Not initiated")				# string with info about the threads


############### Debugging stuff ##################

dir = 1
def pong_step() -> None:
	'''Function to change the sensor value of the debug-sensor'''
	x = sensor.get_proximity()
	if not debug:
		Exception("Not implemented")
	global dir
	if x+0.05 > 1:
		dir = -1
	elif x-0.05 < 0:
		dir = 1
	sensor.__set__(x+0.04*dir)

def debug_input(string:str = "") -> None:
	'''Function to handle the debug specific input'''
	refresh()
	if string == "pong":
		pong_bool.set(not pong_bool.get())
		pong = threading.Thread(target=loop, args=(pong_step, pong_bool, pong_delay))
		pong.start()
		threads.append(pong)

	else:
		try:
			num = float(string)
			sensor.__set__(num)
		except:
			pass

############### Functions ##################

### loop ###

def loop(fkt:function, loop:change_notifier=False,delay:float=1) -> None:
	'''Function to loop a function with specific delay and stop condition'''
	while loop.get():
		fkt()
		time.sleep(delay)


#### Sensor ####

def read_sensor() -> None:
	'''Reads data from sensor and updates UI if necessary'''
	if s.set(sensor.get_proximity()) and m.get() == "auto":
		calc_lights(s.get())

refresh("Sensor initiated")

#### Lights ####

def calc_lights(pos = -1) -> None:
	'''Recalculates all lights and updates the UI'''
	for light in lights.lights:
		light.illuminate(pos)
	refresh()

refresh("Lights initiated")

#### MQTT and mode checker ####

d = f"broker: {mqtt.broker()}, topic: {mqtt.pub_topic()}"
def check_mode() -> None:
	'''Gets mode from file, updated the operating mode of the app and sends the mode via mqtt'''
	# compare mode from file with current mode
	lock.acquire()
	m_file = mode.get().lower()
	lock.release()
	if m.set(m_file):
		# change operating mode if necessary
		change_operation(m_file)
		refresh()
	# Send mode via mqtt
	mqtt.publish(m.get())
	mqtt.log("Mode: " + str(m.get()))

refresh("MQTT initiated")

### Functionality ###

def change_operation(new_mode:str) -> None:
	'''Changes the operating mode of the server'''
	if new_mode == "auto":
		automatic.set(True)
		x = threading.Thread(target=loop, args=(read_sensor, automatic, 0.1))
		threads.append(x)
		x.start()
		calc_lights(s.get())
	else:
		automatic.set(False)

		if new_mode == "on":
			for light in lights.lights:
				light.turn("On")

		elif new_mode == "off":
			for light in lights.lights:
				light.turn("Off")
	refresh()

### input ###

def user_input():
	'''Gets input from the user and initiates all necessary actions'''
	while True:
		string = input().lower()
		if string == "exit":
			break
		elif string in ["on","off","auto"] and m.set(string):
			lock.acquire()
			mode.set(string)
			lock.release()
			change_operation(string)
			continue
		elif debug:
			debug_input(string)
			continue
		
		refresh()
		
refresh("Input initiated")


refresh("Everything initiated")
############### Main  section ##################
if __name__ == "__main__":
	
	# Threads
	refresh("Setting up threads")

	# delay and loop condition for automatic mode
	automatic = change_notifier(False)
	automatic_delay = 0.1

	# delay and loop condition for MQTT and mode checker
	mode_checking = change_notifier(True)
	checking_delay = 1

	# delay and loop condition for pong in debug mode
	pong_bool = change_notifier(False)
	pong_delay = 1

	# list for all threads to terminate the threads properly at the end
	threads = []

	# initiate MQTT and mode checker thread
	ckecker = threading.Thread(target=loop, args=(check_mode, mode_checking, checking_delay))
	threads.append(ckecker)

	# Start thread
	refresh("Starting threads")
	ckecker.start()

	################ Start normal operation mode  ################
	
	user_input()
	

	################ end ################
	refresh("Stopping threads")
	# set all loop conditions to False to stop all threads
	mode_checking.set(False)
	automatic.set(False)
	pong_bool.set(False)

	# wait for threads to stop
	for t in threads:
		t.join()

	refresh("Threads stopped")

	# Disconnect from MQTT
	mqtt.end()

	# return to normal console
	live.stop()