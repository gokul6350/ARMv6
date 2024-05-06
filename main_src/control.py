import game
import time
import serial





port = "/dev/ttyACM0"
connection = serial.Serial(port, 9600)
print(f"Serial {port} is working well")

grup= 60
grdow=0

def wistangle(a1,a2):


    theata=180-a2
    xtheata=a1+theata
    xtheata1=xtheata-90
    wtheata=180-xtheata1

    return wtheata


"""
y
||
||
||
||
||
||
=================x

"""
currentang={"b":10,"s" :110,"e" :110,"f" :90,"w": 180,"g": 60}

def send(ser, ang):
    connection.write(f"{ser}{ang}".encode())
    currentang[ser]=ang

def check(length):
    if 19>length or 33<length:
        print("""
       ___  _   _ _____    ___  _____   ____      _    _   _  ____ _____         _
      / _ \| | | |_   _|  / _ \|  ___| |  _ \    / \  | \ | |/ ___| ____|      /( )\    
     | | | | | | | | |   | | | | |_    | |_) |  / _ \ |  \| | |  _|  _|       / / \ \    __
     | |_| | |_| | | |   | |_| |  _|   |  _ <  / ___ \| |\  | |_| | |___     / /   \ \_ / _\ 
      \___/ \___/  |_|    \___/|_|     |_| \_\/_/   \_\_| \_|\____|_____|   / /     \__O (__
                                                                           / /___       \__/
                                                                          |___ARM|            """)                                                                                                                          
    
        exit()

def pickup(base, x, y):
    check(x)
    base = base + 5
    x = x - 10
    a1, a2 = game.sim_inverse_k(x, y)
    print("=============")
    print("pick up script")
    print(a1, a2)
    print("=============")
    
    x, a2 = -a1, a2
    send("s", 120)
    time.sleep(0.5)
    send("g", grup)
    time.sleep(0.5)
    send("w", 180)
    time.sleep(0.5)
    send("e", a2)
    time.sleep(0.5)
    send("b", base)
    time.sleep(0.5)
    send("s", x)
    wang = wistangle(x, a2)
    print(wang)
    time.sleep(1)
    send("w", wang)
    time.sleep(0.5)
    send("g", grdow)
    time.sleep(0.5)
    send("s", 120)





#pickup(base,length,y)
"""
base=90
length = 25
y=7
grup= 60
grdow=0

# for up and down
pickup(base,length,y-2)
pickup(base,length,y-3)
pickup(base,length,y-4)
pickup(base,length,y-5)
pickup(base,length,y-6)
pickup(base,length,y-7)
pickup(base,length,y-8)
pickup(base,length,y-9)
pickup(base,length,y-10)
pickup(base,length,y-11)
pickup(base,length,y-12)
pickup(base,length,y-13)
pickup(base,length,y-14)
pickup(base,length,y-15)
pickup(base,length,y-16)
pickup(base,length,y-17)

"""

##########################
#  PLACE A OBJECT        #
##########################

def place(base, x, y):
    base = base + 5
    x = x - 8

    a1, a2 = game.sim_inverse_k(x, y)
    print("=============")
    print(a1, a2)
    print("=============")
    
    x, a2 = -a1, a2
    send("s", 120)
    time.sleep(0.5)
   
    time.sleep(0.5)
    send("e", a2)
    time.sleep(0.5)
    send("b", base)
    time.sleep(0.5)
    send("s", x)
    wang = wistangle(x, a2)
    print(wang)
    time.sleep(1)
    send("w", wang)
    time.sleep(0.5)
    send("g", grup)
    time.sleep(0.5)
    send("s", 120)
  

#place(45,23,-5) 
print(currentang)
def openup():
    connection.write(f"g{grup}".encode())

def closedown():
    connection.write(f"g{grdow}".encode())

def move(direction):
    if direction =="left":
        send("b",currentang["b"]-5)
    elif direction =="right":
        send("b",currentang["b"]+5)
    elif direction=="up":
        raise NotImplementedError
    elif direction=="down":
        raise NotImplementedError        

#move("left")        


