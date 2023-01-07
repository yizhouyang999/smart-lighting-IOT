import sys, os, inspect
# Path to the file that stores the mode
p = inspect.getsourcefile(lambda:0)[0:-2]+"txt"

def set(m:str) -> None:
    '''Sets the mode to m'''
    with open(p,"w") as file:
        file.write(m.lower())

def get() -> str:
    '''Returns the mode'''
    with open(p,"r") as file:
        return file.read().lower()

# If the script is run from the command line, set the mode
if __name__ == "__main__":
    if len(sys.argv)>1 and sys.argv[1].lower() in ["on", "off", "auto"]:
        set(sys.argv[1])
    else:
        print("Please enter the mode: [off,on,auto]")