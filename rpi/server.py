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
l = change_notifier("")
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
	if s.set(sensor.get_proximity()):
		lock.acquire()
		refresh()
		lock.release()

th = "Sensor initiated"

#### Lights ####
light_data = change_notifier(True)
light_delay = 0.1

def light():
	return

th = "Lights initiated"

################# Functions ####################

def ui():
	console_ui.lines_add("Enter 'exit' to exit, enter 'on', 'off' or 'auto' to change mode or enter a float to change sensor value while debugging:")
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
		elif string == "refresh":
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

	# Start threads
	th = "Starting threads"
	refresh()
	time.sleep(1)
	sender.start()
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
	# wait for threads to stop
	sender.join()
	th = "Threads stopped"
	refresh()

	# Disconnect from MQTT
	mqtt.end()