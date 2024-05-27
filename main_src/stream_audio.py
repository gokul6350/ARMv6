import pvorca
import sounddevice as sd
import numpy as np
from dotenv import dotenv_values
import struct


env = dotenv_values()
access_key = env["pico"]
model_path = env["pvmd"]


orca = pvorca.create(access_key=access_key, model_path=model_path)

def tts(text):
 
    stream = orca.stream_open()

    pcm = stream.synthesize(text)
    if pcm:
        pcm_bytes = struct.pack('<' + 'h' * len(pcm), *pcm) if isinstance(pcm, list) else pcm
        pcm_array = np.frombuffer(pcm_bytes, dtype=np.int16)
        sd.play(pcm_array, samplerate=22050)
        sd.wait()

   
    pcm = stream.flush()
    if pcm:
        pcm_bytes = struct.pack('<' + 'h' * len(pcm), *pcm) if isinstance(pcm, list) else pcm
        pcm_array = np.frombuffer(pcm_bytes, dtype=np.int16)
        sd.play(pcm_array, samplerate=22050)
        sd.wait()


    stream.close()



