import streamlit as st
import vision
from control import move, pickup, drop, put
import cmd_ui
import angle
import logging
import chat




def act(prompt):
    prompt=chat.gen_ai(prompt)
    if prompt[0] == "_":
        repp = paser(prompt)
        cmd = repp[1]
        respon = repp[0]
        print(f"=====================\n    {prompt} \n=======================     ")
        logging.info(f'cmd: {cmd}')
        objs, origin = vision.cam()
        logging.info(f'Vision.cam: {objs},{origin}')
        main1(cmd, objs, origin)
    else:
        respon = prompt
        logging.info(f'else: {prompt}')
    return respon
def paser(msg):
    original_string = msg
    parts = original_string.split('#')
    first_part = parts[0].strip()
    second_part = parts[1].strip()
    cmd = first_part
    repp = second_part
    return [repp, cmd]

def main1(cxv, objs, origin):
    tokens = cxv.split('(')
    command = tokens[0].strip()
    args = tokens[1].rstrip(')').split(',')

    xxw = objs[str(args[0])]
    b_a = angle.calculate_angle(13.5, 13.5, origin, 13.5, tuple(xxw)[0], tuple(xxw)[1])
    dist = angle.euclidean_distance_2d(xxw, (origin, int(14)))
    print(f'Base angle: {b_a}')
    print(f'distace from origin: {dist}')
    print(f'location of battery: {xxw}')
    print(f'all objects: {objs}')
    if command == '_move':
        move(*args, xxw)
    elif command == '_pickup':
        pickup(dist, b_a)
    elif command == '_drop':
        drop(*args, xxw)
    elif command == '_put':
        put(*args, xxw)
    else:
        print("Invalid syntax")

prompt = "pick up the battery"

full_response = act(prompt)

print(full_response)