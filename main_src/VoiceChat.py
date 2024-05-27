import struct
import pyaudio
import pvporcupine
import wave
import threading
import VAD
import time
from dotenv import dotenv_values
env_vars = dotenv_values()
import requests
import sys

import sounddevice as sd
import soundfile as sf
import stream_audio as sa

import utils
from utils import client2
import client

beep_file=env_vars["beep"]
def preload_audio():
    data, fs = sf.read(beep_file)
    return data, fs
audio_data, sample_rate = preload_audio()

def play_audio():
    
    sd.play(audio_data, sample_rate)
    sd.wait()

porcupine = None

pa = None

audio_stream = None
recording = False
hot_detected = False
record_stopped = False
triggered = False

def stop_recording():
    global recording, record_stopped
   
    recording = False
    record_stopped = True
   

def clear_last_n_lines(n):
    
    for _ in range(n):
        sys.stdout.write('\x1b[1A')  
        sys.stdout.write('\x1b[2K')  
    sys.stdout.flush()



try:
    porcupine = pvporcupine.create(keywords=["computer", "jarvis"],)
    pa = pyaudio.PyAudio()
    audio_stream = pa.open(
        rate=porcupine.sample_rate,
        channels=1,
        format=pyaudio.paInt16,
        input=True,
        frames_per_buffer=porcupine.frame_length
    )
    clear_last_n_lines(12)
    print("Say jarvis/computer to listen ")
    while True:
        frames = []

        recording = False
        hot_detected = False
        record_stopped = False
        triggered = False
        silence_start=0


        while True:
            pcm = audio_stream.read(porcupine.frame_length)
            pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)

            if not hot_detected:
                keyword_index = porcupine.process(pcm)
                if keyword_index >= 0:
                    try:
                        obj,oj,fr=client.handshake()  
                        del oj,fr 
                        #print(obj)
                        if obj == None or obj =={}:
                            obj="none "
                        else:
                            obj=','.join(obj.keys()) 
                    except Exception as e:
                        obj= "none 1"
                    #print(obj)
                    audio_thread = threading.Thread(target=play_audio)
                    audio_thread.start()

                    recording = True
                    hot_detected = True

            if recording:
                frames.append(pcm)
               
                is_speech=VAD.dectect_speech(pcm) 
                if is_speech:
                    triggered = False
                else:
                    
                    if not triggered:
                        triggered = True
                        silence_start = time.time()
                    else:
                        triggered = True

                       
                if (triggered == True) and (time.time() - silence_start) > 1:
                    audio_thread = threading.Thread(target=play_audio)
                    audio_thread.start()
                    stop_recording()
                    break
            elif record_stopped:
                break
                    
        if record_stopped: 
            with wave.open("recorded_audio.wav", "wb") as wav_file:
                wav_file.setnchannels(1)
                wav_file.setsampwidth(pa.get_sample_size(pyaudio.paInt16))
                wav_file.setframerate(porcupine.sample_rate)
                
                byte_frames = b"".join(struct.pack("h" * len(frame), *frame) for frame in frames)
                wav_file.writeframes(byte_frames)

        #print(obj)
        Text,reply=client2("recorded_audio.wav",obj)
        if reply[0] == "_":
            rep,cmd=utils.paser(reply)
           # print(rep,cmd)
           # print(">>>0<<<")
            action_=threading.Thread(target=utils.act,args=(cmd,))
            action_.start()
        else:
            rep=reply
        tts_thread=threading.Thread(target=sa.tts,args=(rep,))
        tts_thread.start()

        print(f"\n[HUMAN]-{Text}\n[ROBOT]-{rep}")
    
    
except Exception as e:
    print(f"Error: {e}")
except KeyboardInterrupt:
    porcupine.delete()
    VAD.cobra.delete()

    print("shutting Down")
finally:
    if audio_stream is not None:
        audio_stream.close()
    if pa is not None:
        pa.terminate()
