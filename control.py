def move(xyz):
    print(f"Moving to {xyz}")

def pickup(xyz,adw):
    print(f"Pick up {xyz}")

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