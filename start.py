import cam as cm
from control import move, pickup, pick_place, drop, put
import cmd_ui
import angle


print("Welcome to the Robot Arm Control System!")
while True:
    #objs, cenn_,right =  {'battery': (128, 196)}, [388.0, 73.5],[13.5,13.5]
    objs,cen = cm.camera()  
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
    b_a=angle.calculate_angle(13.5,13.5,cen,13.5,tuple(xxw)[0],tuple(xxw)[1])
    
    print(f"feeffe",args, xxw)
    dist=angle.euclidean_distance_2d(xxw,(cen,int(13.5)))

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
     
