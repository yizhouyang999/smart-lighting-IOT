import board
import busio
import adafruit_vcnl4010
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_vcnl4010.VCNL4010(i2c)

def get_proximity() -> float:
	return sensor.proximity/65535.0

def __set__():
	return