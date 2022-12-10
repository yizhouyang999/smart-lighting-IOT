import time

import mode
import sensor
from mqtt import mqtt_server
import console_ui


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

sending_data = change_notifier(True)
sending_delay = 1

m = change_notifier()
def send_data():
	if m.set(mode.get()):
		console_ui.lines[2] = f"Mode: {mode.get()}"
		console_ui.print_data()

	# Send values
	lock.acquire()
	mqtt.client.publish(mqtt.pub_topic, str(m.get()))
	lock.release()
	mqtt.logger.info("Mode: " + str(m.get()))

################# Functions ####################

def ui():
	console_ui.lines_add("Press enter to stop, enter 'log' to toggle logging, enter 'set' ___ to set mode to ___")
	while True:
		s = input()
		console_ui.log_add("User input: " + s)
		if s == "":
			break
		elif s == "log":
			console_ui.toggle_logging()
		elif s[:4] == "set ":
			lock.acquire()
			mode.set(s[4:])
			lock.release()
			console_ui.lines[2] = f"Mode: {mode.get()}"
	
def loop(fkt, loop=False,delay=1):
	while loop.get():
		fkt()
		time.sleep(delay)


############### Main  section ##################
if __name__ == "__main__":
	################ start ################
	# mqtt setup
	broker = "test.mosquitto.org"	# Broker
	pub_topic = "iot_project"       # send messages to this topic
	mqtt = mqtt_server(broker, pub_topic)
	console_ui.lines_add("MQTT: " + broker + '/' + pub_topic)
	mqtt.start()
	client = mqtt.client

	# Threads
	sender = threading.Thread(target=loop, args=(send_data, sending_data, sending_delay))

	# Start threads
	sender.start()

	console_ui.lines.append("Threads started")
	console_ui.lines_add("")

	################ everything running ################
	ui()
	


	################ end ################
	console_ui.lines_add("Stopping threads")
	sending_data.set(False)
	# wait for threads to stop
	sender.join()
	console_ui.lines_add("Threads stopped")

	# Disconnect from MQTT
	mqtt.end()
	console_ui.end()