import streamlit as st
import vision
from control import move, pickup, drop, put
import cmd_ui
import angle
import logging
import chat
import cv2
from datetime import datetime
import stack
import copy
import numpy as np
# Configure the logging module
logging.basicConfig(filename='logfile.txt', level=logging.INFO, format='%(asctime)s - %(message)s')
logging.info('ds=================================')

st.title("NLP ARM CONTROL SYSTEM")

def _alert(mssg):
    rich.print(f"[bold red]alert {mssg} [/bold red]")


def act(prompt):
    #prompt=chat.gen_ai(prompt1)
   # print(f"======================= \n   IN {prompt1} \n OUT  {prompt}")
    if prompt[0] == "_":
        repp = paser(prompt)
        cmd = repp[1]
        respon = repp[0]
        print(f"=====================\n    {prompt} \n=======================     ")
        logging.info(f'cmd: {cmd}')
        objs, origin,frame = vision.cam()
        #if frame == None:
        #    _alert("Frame is a Nonetype")
        logging.info(f'Vision.cam: {objs},{origin}')
        main1(cmd, objs, origin,frame)
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
def frame_2(frame,data):
    height, width, channels = frame.shape


    new_frame = np.ones((height, width, channels), dtype=np.uint8) * 255


    text1 = str(data[0])
    text2 = str(data[1])
    text3 = str(data[2])

    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    font_thickness = 2
    font_color = (0, 0, 0)  


  #  text1_position = (int((width - len(text1) * 20) / 2), int(height / 3))
   # text2_position = (int((width - len(text2) * 20) / 2), int(height / 2))
   # text3_position = (int((width - len(text3) * 20) / 2), int(2 * height / 3))

    cv2.putText(new_frame, text1, (14,150), font, font_scale, font_color, font_thickness, cv2.LINE_AA)
    cv2.putText(new_frame, text2, (14,250), font, font_scale, font_color, font_thickness, cv2.LINE_AA)
    cv2.putText(new_frame, text3, (14,300), font, font_scale, font_color, font_thickness, cv2.LINE_AA)
    return new_frame
def main1(cxv, objs, origin,frame):
    tokens = cxv.split('(')
    command = tokens[0].strip()
    args = tokens[1].rstrip(')').split(',')
    current_time = datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
    xxw = objs[str(args[0])]
    #cv2.imwrite(f'logs/obj3-{formatted_time}.jpg',frame)
    #b_a = angle.calculate_angle(13.5, 13.5, origin, 13.5, tuple(xxw)[0], atuple(xxw)[1])
    
    print(xxw,origin,int(13.5),(0, 255, 0),4)
    frame1=copy.deepcopy(frame)
    frame2=copy.deepcopy(frame)
    ###BASE####
    cv2.line(frame2,(13, 13),(int(origin), 13), (0, 255, 0), 4)
    
    cv2.line(frame2, xxw, (int(origin),14), (0, 255, 0), 4)

    b_a = angle.calculate_angle(int(origin),13,13,13,tuple(xxw)[0], tuple(xxw)[1])
    # just checking
  
    # print("========================")
    # print(angle.calculate_angle(13,13,int(origin),13, tuple(xxw)[0], tuple(xxw)[1]))
    # print(angle.calculate_angle(tuple(xxw)[0], tuple(xxw)[1],13,13,int(origin),13))
    # print(angle.calculate_angle(13,13,tuple(xxw)[0], tuple(xxw)[1],int(origin),13))
    # print(angle.calculate_angle(int(origin),13,13,13,tuple(xxw)[0], tuple(xxw)[1]))
    # print("========================")
    
    ###END###
    dist = angle.euclidean_distance_2d(xxw,(int(origin),14))
    data=(dist,b_a,objs)
    frame1=frame_2(frame=frame,data=data)
    imgstack=stack.stackImages(0.6,([frame,frame1,frame2]))
    cv2.imwrite(f'logs/obj-line {formatted_time}.jpg',imgstack)
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

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):

        st.markdown(prompt)
    with st.chat_message("assistant"):
        message_placeholder = st.empty()

        full_response = chat.gen_ai(prompt=prompt) 
        r_p=act(full_response)
        st.markdown(r_p)

# if __name__ == "__main__":
#    # st.experimental_run_async(main1, (cmd_ui.main(),))
#     st.experimental_run_async(vision.cam)