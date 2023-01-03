############### MQTT section ##################
import paho.mqtt.client as pm
import logging

# create a logger for mqtt
logging.basicConfig(filename="logs/mqtt.log", level=logging.INFO, format="%(asctime)s: %(message)s", filemode='w')
logger = logging.getLogger()

class mqtt_server:
	def __init__(self, broker = None, pub_topic = None):
		'''Initiates the mqtt client and connects to the broker'''
		# Set MQTT broker and topic
		self.broker = broker
		self.pub_topic = pub_topic
		logger.info(f"Initiated with broker={broker}, pub_topic={pub_topic}")

		self.client = pm.Client()

		# Overwrite default functions
		def on_connect(client, userdata, flags, rc) -> None:
			if rc==0:
				logger.info("Connection established. Code: "+str(rc))
			else:
				logger.error("Connection failed. Code: " + str(rc))
				
		self.client.on_connect = on_connect
				
		def on_publish(client, userdata, mid) -> None:
			logger.info("Published: " + str(mid)+"\n")

		self.client.on_publish = on_publish
			
		def on_disconnect(client, userdata, rc) -> None:
			if rc != 0:
				logger.error("Unexpected disonnection. Code: ", str(rc))
			else:
				logger.info("Disconnected. Code: " + str(rc))

		self.client.on_disconnect = on_disconnect
			
		def on_log(client, userdata, level, buf) -> None:		# Message is in buf
			logger.info("MQTT Log: " + str(buf))
			
		self.client.on_log = on_log

		# Connect to broker
		self.client.connect(self.broker)	# Broker address, port and keepalive (maximum period in seconds allowed between communications with the broker)
		
		# Start included loop
		self.client.loop_start()

		logger.info("MQTT client started")

	def end(self) -> None:
		'''Disconnects from the broker and stops the loop'''
		self.client.loop_stop()
		self.client.disconnect()
		logger.info("MQTT client stopped")
	
s = mqtt_server("test.mosquitto.org", "iot_project")

def log(string:str) -> None:
	'''Logs a message to the mqtt log'''
	logger.info(string)

def publish(string) -> None:
	'''Publishes a message to the mqtt topic'''
	s.client.publish(s.pub_topic, string)

def broker() -> str:
	'''Returns the broker'''
	return s.broker

def pub_topic() -> str:
	'''Returns the pub_topic'''
	return s.pub_topic

def end() -> None:
	'''Stops the mqtt client'''
	s.end()