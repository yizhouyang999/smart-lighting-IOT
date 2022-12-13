############### MQTT section ##################
import paho.mqtt.client as pm
import time
import os
import logging


class mqtt_server:
	def __init__(self, broker, pub_topic):
		logging.basicConfig(filename="logs/mqtt.log", level=logging.INFO, format="%(asctime)s: %(message)s", filemode='w')
		self.logger = logging.getLogger()
		self.logger.info("Starting MQTT client")
		# Set MQTT broker and topic
		self.broker = broker
		self.pub_topic = pub_topic
		# make client
		self.client = None
	# override logging functions
	def start(self):
		self.client = pm.Client()
		self.client.connect(self.broker)	# Broker address, port and keepalive (maximum period in seconds allowed between communications with the broker)
		self.client.loop_start()
		def on_connect(client, userdata, flags, rc):
			if rc==0:
				self.logger.info("Connection established. Code: "+str(rc))
			else:
				self.logger.error("Connection failed. Code: " + str(rc))
				
		self.client.on_connect = on_connect
				
		def on_publish(client, userdata, mid):
			self.logger.info("Published: " + str(mid)+"\n")
			client.on_publish = on_publish
			
		def on_disconnect(client, userdata, rc):
			if rc != 0:
				self.logger.error("Unexpected disonnection. Code: ", str(rc))
			else:
				self.logger.info("Disconnected. Code: " + str(rc))
			client.on_disconnect = on_disconnect
			
		def on_log(client, userdata, level, buf):		# Message is in buf
			self.logger.info("MQTT Log: " + str(buf))
			client.on_log = on_log
		self.logger.info("MQTT client started")

	def end(self):
		self.client.loop_stop()
		self.client.disconnect()