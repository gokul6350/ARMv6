import argparse
import sys
import struct
import wave
from threading import Thread
import pyaudio
import pvcobra

from dotenv import dotenv_values
env_vars = dotenv_values()

"""
try:
    


    audio_interface = pyaudio.PyAudio()
    stream = audio_interface.open(
                rate=16000,
                format=pyaudio.paInt16,
                channels=1,
                input=True,
                frames_per_buffer=512,
                )

except Exception as e:
     print(e)
"""
cobra = pvcobra.create(access_key=env_vars["pico"])
def dectect_speech(pcm):
        
    voice_probability = cobra.process(pcm)
    percentage = voice_probability * 100
    bar_length = int((percentage / 10) * 3)
    empty_length = 30 - bar_length
    sys.stdout.write("\r[%3d]|%s%s|" % (
        percentage, '█' * bar_length, ' ' * empty_length))
    sys.stdout.flush()

    if percentage < 96:
        return False
    else:
        return True
