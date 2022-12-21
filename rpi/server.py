import time

import mode
import sensor
import lights
from mqtt import mqtt_server
import console_ui
from rich import padding


############### Threads ##################
import threading
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

m = change_notifier("")
s = change_notifier(0)
d = "---"
l = change_notifier(lights.lights)
th = "Not initiated"

# easy way to refresh console
def refresh():
	console_ui.print_data(m.get(),s.get(),d,l.get(),th)

refresh()
#### MQTT ####
sending_data = change_notifier(True)
sending_delay = 1

def send_data():
	if m.set(mode.get()):
		lock.acquire()
		refresh()
		lock.release()

	# Send values
	lock.acquire()
	mqtt.client.publish(mqtt.pub_topic, str(m.get()))
	lock.release()
	mqtt.logger.info("Mode: " + str(m.get()))

th = "Sender initiated"

#### Sensor ####
reading_data = change_notifier(True)
reading_delay = 0.1

def read_data():
	'''Reads data from sensor and updates UI if necessary'''
	if s.set(sensor.get_proximity()):
		refresh()

th = "Sensor initiated"

#### Calculation ####
light_data = change_notifier(True)
light_delay = 0.1

def calc():
	pos = s.get()
	f5 = False
	for light in lights.lights:
		if light.illuminate(pos) and not light.on:
			light.turn("On")
			f5 = True
		elif not light.illuminate(pos) and light.on:
			light.turn("Off")
			f5 = True
	if f5:
		refresh()
th = "Lights initiated"

move_data = change_notifier(False)
move_delay = 1

dir = 1
def move_pos():
	global dir
	if s.get()+0.05 > 1:
		dir = -1
	elif s.get()-0.05 < 0:
		dir = 1
	s.set(s.get()+dir*0.04)

################# Functions ####################

def ui():
	while True:
		string = input()
		if string == "exit":
			break
			#sensor.__set__(float(s[6:]))
		elif string in ["on","off","auto"]:
			lock.acquire()
			mode.set(string)
			lock.release()
			refresh()
		elif string == "r":
			refresh()
		# just for debugging
		else:
			try:
				num = float(string)
				s.set(num)
				refresh()
			except:
				print("Invalid input")
			

th = "UI initiated"

def loop(fkt, loop=False,delay=1):
	while loop.get():
		fkt()
		time.sleep(delay)

th = "Everything initiated"
############### Main  section ##################
if __name__ == "__main__":
	################ start ################
	# mqtt setup
	broker = "test.mosquitto.org"	# Broker
	pub_topic = "iot_project"       # send messages to this topic
	mqtt = mqtt_server(broker, pub_topic)
	mqtt.start()
	client = mqtt.client
	d = "broker: " + broker + ", topic: " + pub_topic
	# Threads
	th = "Setting up threads"
	sender = threading.Thread(target=loop, args=(send_data, sending_data, sending_delay))
	proximity = threading.Thread(target=loop, args=(read_data, reading_data, reading_delay))
	light = threading.Thread(target=loop, args=(calc, light_data, light_delay))
	pong = threading.Thread(target=loop, args=(move_pos, move_data, move_delay))

	# Start threads

	sending_data.set(True)
	reading_data.set(True)
	light_data.set(True)
	move_data.set(False)
	
	th = "Starting threads"
	refresh()
	sender.start()
	# proximity.start()
	light.start()
	pong.start()
	th = "Threads started"
	refresh()

	################ everything running ################
	ui()
	


	################ end ################
	th = "Stopping threads"
	refresh()
	sending_data.set(False)
	reading_data.set(False)
	light_data.set(False)
	move_data.set(False)
	# wait for threads to stop
	sender.join()
	th = "Threads stopped"
	refresh()

	# Disconnect from MQTT
	mqtt.end()