import cam as cm
from control import move, pickup, pick_place, drop, put
import cmd_ui
import angle
import game

print("Welcome to the Robot Arm Control System!")
while True:
    objs, cenn_,right = cm.camera() #{'battery': (128, 196)}, [388.0, 73.5]  
    objs1 = f"Objects found {objs}"
    print(objs1, cenn_)

    cxv = cmd_ui.main(objs1)
    print(cxv)
    tokens = cxv.split('(')
    command = tokens[0].strip()
    args = tokens[1].rstrip(')').split(',')
    print(str(args[0]))
    # Strip extra spaces and quotes around the arguments



    xxw = objs[str(args[0])]
    print(angle.calculate_angle(tuple(xxw)[0],tuple(xxw)[1],cenn_[0],cenn_[1],right[0],right[1]))
    
    print(f"feeffe",args, xxw)
    dist=angle.euclidean_distance_2d(xxw,(int(0),int(13.5)))

    game.sim_inverse_k(dist/10,0)
    print(dist/10)
    if command == '_move':
        move(*args,xxw)
    elif command == '_pickup':
        pickup(*args,xxw)
    elif command == '_drop':
        drop(*args,xxw)
    elif command == '_put':
        put(*args,xxw)
    elif command.startswith('_pick'):
        pick_place(*args,xxw)
    else:
        print("Invalid syntax")
     
