import client
import threading
import cv2
import numpy as np
import copy
import stack
import control
from datetime import datetime



import angle
import requests
from dotenv import dotenv_values
env_vars = dotenv_values()
import time
from log import log1,log2,log3
from stream_audio import tts

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
   # print(cxv, objs, origin,frame)
    tokens = cxv.split('(')
    command = tokens[0].strip()
    args = tokens[1].rstrip(')').split(',')
    current_time = datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
   # new_dict = {"box1": [[0, 0]], "box2": [[1, 1]]}
    #objs.append(new_dict)

    objs["box1"]=[[0, 0]]
    objs["box2"]=[[1, 1]]
    objs["box"]=[[0, 0]]

    try:
        xxw = objs[str(args[0])]
        xxw=tuple(xxw[0])
    except Exception as e:
        print(f"OBJECT NOT FOUND  ")
        tts("OBJECT NOT FOUND  ")
    #cv2.imwrite(f'logs/obj3-{formatted_time}.jpg',frame)
    #b_a = angle.calculate_angle(13.5, 13.5, origin, 13.5, tuple(xxw)[0], atuple(xxw)[1])
    
   # print(xxw,origin,int(13.5),(0, 255, 0),4)
    frame1=copy.deepcopy(frame)
    frame2=copy.deepcopy(frame)
    ###BASE####
   # print(frame2, xxw, (int(origin),14), (0, 255, 0), 4)
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
    dist = round(dist/10, 1)  # Round to 1 decimal place
   
   # print("=================")

  # log2(f"BASE ANGLE {b_a}")

   # log2(f"distance {dist}")
   # print("=================")
    cv2.imwrite(f'logs/obj-line {formatted_time}.jpg',imgstack)
    if command == '_move':
        control.move()
       # move(*args, xxw)
    elif command == '_pickup':
        control.pickup(base=b_a,x=dist,y=9.5) 
    elif command == '_drop':
        control.drop()
    elif command == '_put':
      #  put(*args, xxw)
     # log2(f"TRAGETED BOX {str(args[0])}")
      if str(args[0]) == "box2":
        control.place(base=50,x=31,y=-3)
        
      else:
        control.place(base=30,x=23,y=-3)
    else:
        print("Invalid syntax")


def act(cmd):

        
        objs, origin,frame = client.handshake()
            #thread = threading.Thread(target=main1, args=(cmd, objs, origin,frame))
       # print(cmd)
        main1(cmd,objs,origin,frame)



            #thread.start()
   


        #return respon

def client2(file_path, text):
    upload_url = env_vars["transcribe_server"]
   # print(f"dfsffef {text} , {type(text)}")
    try:
        with open(file_path, "rb") as file:
            files = {"file": file}
            data = {"text": text}

            start_time = time.time()
            response = requests.post(upload_url, files=files, data=data)
            end_time = time.time()

        elapsed_time = end_time - start_time

        response.raise_for_status()  # This will raise an exception for HTTP errors

        json_obj = response.json()

        transcribed_text = json_obj["text"]
        reply = json_obj["reply"]
            
        return transcribed_text, reply
    except requests.exceptions.RequestException as e:
        print("\n $$$$>Error in Transcribe Server \n", e)
        



#rep,cmd=paser("_pickup(battery) # picking up the battery")
#print(rep,cmd)
#act(cmd)