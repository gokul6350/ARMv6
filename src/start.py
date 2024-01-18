import vision 
from control import move, pickup, pick_place, drop, put
import cmd_ui
import angle
import threading
import sys
print("Welcome to the Robot Arm Control System!")
#vision.cam()
import logging

logging.basicConfig(level=logging.DEBUG)


def main():
    while True:
        #objs, origin, =  {'battery': (128, 196)}, [388.0, 73.5],[13.5,13.5]
        objs,origin=vision._Objects()
        objs1 = f"Objects found {objs}"
        print(objs1)

        cxv = cmd_ui.main(objs1)
        print(cxv)
        tokens = cxv.split('(')
        command = tokens[0].strip()
        args = tokens[1].rstrip(')').split(',')
        print(str(args[0]))
        right=(int(13.5), int(13.5))
        # Strip extra spaces and quotes around the arguments



        xxw = objs[str(args[0])]
        b_a=angle.calculate_angle(13.5,13.5,origin,13.5,tuple(xxw)[0],tuple(xxw)[1])
        
        print(f"feeffe",args, xxw)
        dist=angle.euclidean_distance_2d(xxw,(origin,int(13.5)))

    # game.sim_inverse_k(dist/10,0)
        print(dist/10)
        if command == '_move':
            move(*args,xxw)
        elif command == '_pickup':
            pickup(dist,b_a)
        elif command == '_drop':
            drop(*args,xxw)
        elif command == '_put':
            put(*args,xxw)
        #elif command.startswith('_pick'):
        #   pick_place(*args,xxw)
        else:
            print("Invalid syntax")
     

if __name__ == "__main__":
    # Configure logging for the specific thread (t2 in this case)
    logging.getLogger('vision.cam').setLevel(logging.WARNING)  # Adjust the logger name as needed
    
    t1 = threading.Thread(target=main)
    t2 = threading.Thread(target=vision.cam)     

    # Start the threads
    t1.start()
    t2.start()

    # Wait for both threads to finish
    t1.join()
    t2.join()
