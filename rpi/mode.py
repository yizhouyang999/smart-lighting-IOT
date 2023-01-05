import sys
def set(m:str) -> None:
    with open("/home/pi/Documents/mode.txt","w") as file:
        file.write(m.lower())

def get() -> str:
    with open("/home/pi/Documents/mode.txt","r") as file:
        return file.read().lower()

if __name__ == "__main__":
    if len(sys.argv)>1 and sys.argv[1].lower() in ["on", "off", "auto"]:
        set(sys.argv[1])
    else:
        print("Please enter the mode: [off,on,auto]")