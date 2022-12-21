# import board
# import busio
# import adafruit_vcnl4010
# i2c = busio.I2C(board.SCL, board.SDA)

# For debugging without sensor
p = None
def __set__(x):
	global p
	p = x

# sensor = adafruit_vcnl4010.VCNL4010(i2c)	# Proximity	
def get_proximity():
	# if p != None:
	return p
	# return sensor.proximity/65535 # The higher the value, object closer to sensor
	