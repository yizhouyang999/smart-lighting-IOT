import sys
def set(m):
    with open("mode.txt","w") as file:
        file.write(m)

def get():
    with open("mode.txt","r") as file:
        return file.read()

if __name__ == "__main__":    
    if sys.argv[1] in ["on", "off", "auto"]:
        set(sys.argv[1])
    else:
        print("Please enter the mode: [off,on,auto]")