#!pip install gTTS


from gtts import gTTS
tts = gTTS('Write hello in English to hello.mp3:', lang='en')
tts.save('hello3.mp3')