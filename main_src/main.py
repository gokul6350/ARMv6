import gradio as gr
print(gr.__version__)
#from discordwebhook import Discord
import requests
import time
import json
import chat
from rich import print
import control
import client
import copy 
import cv2 
import threading


from datetime import datetime
from log import log1,log2,log3
from elevenlabs import play , save,stream
from elevenlabs.client import ElevenLabs
import uuid
import angle
import numpy as np
import stack
import matplotlib
matplotlib.use("agg")
from dotenv import dotenv_values
env_vars = dotenv_values()
import time
from functools import wraps
# Load environment variables from .env file

global audipth
def send_(level, message):
  #  discord.post(content=f"[{level}]: {message}")
   pass

def measure_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        log3(f"Function {func.__name__} executed in {execution_time:.4f} seconds")
        return result
    return wrapper
def act(prompt):
    #prompt=chat.gen_ai(prompt1)
   # print(f"======================= \n   IN {prompt1} \n OUT  {prompt}")
    if prompt[0] == "_":
        repp = paser(prompt)
        cmd = repp[1]
        respon = repp[0]
        print(f"=====================\n    {prompt} \n=======================     ")
       # logging.info(f'cmd: {cmd}')
       #old objs, origin,frame = vision.cam()
        if '#' in prompt:
            objs, origin,frame = client.handshake()
        #if frame == None:
        #    _alert("Frame is a Nonetype")
       # logging.info(f'Vision.cam: {objs},{origin}')
            thread = threading.Thread(target=main1, args=(cmd, objs, origin,frame))



            #main1(cmd, objs, origin,frame)
            thread.start()
        else:
            respon = " Doing it"  
            log1("WARNING: # in the sentence")  
    else:
        respon = prompt
        #logging.info(f'else: {prompt}')
    return respon
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

@measure_time
def main1(cxv, objs, origin,frame):
    tokens = cxv.split('(')
    command = tokens[0].strip()
    args = tokens[1].rstrip(')').split(',')
    current_time = datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
   # new_dict = {"box1": [[0, 0]], "box2": [[1, 1]]}
    #objs.append(new_dict)

    objs["box1"]=[[0, 0]]
    objs["box2"]=[[1, 1]]

    try:
        xxw = objs[str(args[0])]
        xxw=tuple(xxw[0])
    except Exception as e:
        print(f"OBJECT NOT FOUND   {e}")
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

    log2(f"BASE ANGLE {b_a}")

    log2(f"distance {dist}")
   # print("=================")
    cv2.imwrite(f'logs/obj-line {formatted_time}.jpg',imgstack)
    if command == '_move':
        control.move()
       # move(*args, xxw)
    elif command == '_pickup':
        control.pickup(base=b_a,x=dist,y=7.5) 
    elif command == '_drop':
        control.drop()
    elif command == '_put':
      #  put(*args, xxw)
      log2(f"TRAGETED BOX {str(args[0])}")
      if str(args[0]) == "box2":
        control.place(base=50,x=31,y=-3)
        
      else:
        control.place(base=30,x=23,y=-3)
    else:
        print("Invalid syntax")

def paser(msg):
    
    original_string = msg
    parts = original_string.split('#')
    first_part = parts[0].strip()
    second_part = parts[1].strip()
    cmd = first_part
    repp = second_part
    return [repp, cmd]

# Example usage
@measure_time
def client2(file_path):
    upload_url = env_vars["transcribe_server"]

    # Open the audio file in binary mode
    with open(file_path, "rb") as file:
       
        files = {"file": file}
        
        
        start_time = time.time()
        
      
        response = requests.post(upload_url, files=files)
        
      
        end_time = time.time()

   
    elapsed_time = end_time - start_time
    send_("INFO",f"res: {response} and completed in {elapsed_time} ")
    json_obj = response.json()

        # Extract the value associated with the key "text"
    text = json_obj["text"]
        
    return text
   
  

#chat = Chat(system="You are a helpful assistant.")
@measure_time
def run_prompt(text):
    objs, origin,frame = client.handshake()
    full_response = chat.gen_ai(prompt=f"you can see {objs}.  {text}") 
    print(f"======================= \n   IN you can see {objs}. {text} \n OUT  {full_response}")
    r_p=act(full_response)	
   # discord2.post(content=f"{r_p}")
    log1(f"RESPONCES FOR LLM: {r_p}")
    return r_p


client1 = ElevenLabs(api_key=  env_vars["elevenlabs_key"],)
@measure_time
def run_text_prompt(message, chat_history):
    if message[0] == "_":
        rep=act(message[1:]) # will skip the LLM part
    else:
        rep = run_prompt(message)
 #   discord2.post(content=f"{rep}")
    log1(f"RESPONCES FOR LLM: {rep}")
    audio = client1.generate(
        text=rep,
        voice="Josh",
        model="eleven_multilingual_v2"
    )
    
    threadaudio = threading.Thread(target=play, args=(audio,))



            #main1(cmd, objs, origin,frame)
    threadaudio.start()
    #play(audio)
    
    chat_history.append((message, rep))
    return "", chat_history


def run_audio_prompt(audio, chat_history):
    if audio is None:
        return None, chat_history
    else:
        text=client2(audio)
   # message_transcription = model.transcribe(audio)["text"]
    _, chat_history = run_text_prompt(text, chat_history)
    log1("TRANS ADDED")
    return None, chat_history


with gr.Blocks(title="ROBOTIC ARM LLM") as demo:
    chatbot = gr.Chatbot(height=650)

    msg = gr.Textbox()
    msg.submit(run_text_prompt, [msg, chatbot], [msg, chatbot])
    chatbot.change()
    with gr.Row():
        audio = gr.Audio(sources="microphone", type="filepath")
        
        send_audio_button = gr.Button("Send Audio", interactive=True)
        send_audio_button.click(run_audio_prompt, [audio, chatbot], [audio, chatbot])

demo.launch(favicon_path="icon.png",share=True)
     