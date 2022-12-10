# import board
# import busio
# import adafruit_vcnl4010
# i2c = busio.I2C(board.SCL, board.SDA)

# sensor = adafruit_vcnl4010.VCNL4010(i2c)	# Proximity	
def get_proximity():
	proximity = 0#sensor.proximity # The higher the value, object closer to sensor
	#print('Proximity: {0}'.format(proximity))
	return proximity