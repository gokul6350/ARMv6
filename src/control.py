import game
#import arduinoserial2 as as2

#as2.detect()
#conection=as2.connect()
#The above code will automaticaly detect the arduino uno board and will have default baud rate 9600
def move(dis,base):
    #print(f"Moving to {obj}")
    print(dis)
    a1,b1=game.sim_inverse_k(dis/10,2)
   # as2.send_data(conection,f"b{base}")
    print(f"sending b{base}")

def pickup(dis,base):
    print(dis)
    a1,b1=game.sim_inverse_k(int(dis/10),-2)
    print(base)
 #   as2.send_data(conection,f"b{base}")
    print(f"sending b{base}")

def drop(xyz):
    print(f"Drop {xyz}")

def put(xyz):
    print(f"Put {xyz}")

def pick_place(xyz, abc):
    print(f"Pick {xyz} and place {abc}")

"""def execute_syntax(syntax):
    tokens = syntax.split('(')
    command = tokens[0].strip()
    args = tokens[1].rstrip(')').split(',')
    args = [arg.strip() for arg in args]

    if command == '_move':
        move(*args)
    elif command == '_pickup':
        pickup(*args)
    elif command == '_drop':
        drop(*args)
    elif command == '_put':
        put(*args)
    elif command.find() == '_pick':
        pick_place(*args)
    else:
        print("Invalid syntax")

"""