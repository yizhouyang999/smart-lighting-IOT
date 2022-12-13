import os
import time
from rich import print
lines = []
logs = []
logging = False

def toggle_logging():
    global logging
    logging = not logging
    print_data()
	
def print_data():
	os.system('cls' if os.name == 'nt' else 'clear')
	for line in lines:
		print(line)
	if logging:
		print("\n","#"*20,"MQTT LOGS","#"*20,"\n")
		for line in logs:
			print(line)

def lines_add(x, list = lines):
	list.append(x)
	print_data()

def log_add(s):
	logs.append(s)
	if logging:
		print(s)
def end():
    if logging:
        with open(f"logs/log{hash(time.time())}.log","w") as file:
            file.write(f'''{time.asctime()}:\n\n''')
            for line in logs:
            	file.write(line+"\n")
