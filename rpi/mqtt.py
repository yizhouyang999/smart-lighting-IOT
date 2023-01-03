############### MQTT section ##################
import paho.mqtt.client as pm
import logging

logging.basicConfig(filename="logs/mqtt.log", level=logging.INFO, format="%(asctime)s: %(message)s", filemode='w')
logger = logging.getLogger()
class mqtt_server:
	def __init__(self, broker = None, pub_topic = None):
		# Set MQTT broker and topic
		self.broker = broker
		self.pub_topic = pub_topic
		# make client
		self.client = None
		logger.info(f"Initiated with broker={broker}, pub_topic={pub_topic}")
	# override logging functions
	def start(self):
		self.client = pm.Client()

		def on_connect(client, userdata, flags, rc):
			if rc==0:
				logger.info("Connection established. Code: "+str(rc))
			else:
				logger.error("Connection failed. Code: " + str(rc))
				
		self.client.on_connect = on_connect
				
		def on_publish(client, userdata, mid):
			logger.info("Published: " + str(mid)+"\n")

		self.client.on_publish = on_publish
			
		def on_disconnect(client, userdata, rc):
			if rc != 0:
				logger.error("Unexpected disonnection. Code: ", str(rc))
			else:
				logger.info("Disconnected. Code: " + str(rc))

		self.client.on_disconnect = on_disconnect
			
		def on_log(client, userdata, level, buf):		# Message is in buf
			logger.info("MQTT Log: " + str(buf))
			
		self.client.on_log = on_log

		self.client.connect(self.broker)	# Broker address, port and keepalive (maximum period in seconds allowed between communications with the broker)
		self.client.loop_start()

		logger.info("MQTT client started")

	def end(self):
		self.client.loop_stop()
		self.client.disconnect()
		logger.info("MQTT client stopped")
	
s = mqtt_server("test.mosquitto.org", "iot_project")
s.start()

def log(string):
	'''Logs a message to the mqtt log'''
	logger.info(string)

def publish(string):
	'''Publishes a message to the mqtt topic'''
	s.client.publish(s.pub_topic, string)

def broker():
	'''Returns the broker'''
	return s.broker

def pub_topic():
	'''Returns the pub_topic'''
	return s.pub_topic
	
def end():
	'''Stops the mqtt client'''
	s.end()