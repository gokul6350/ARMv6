import requests

url = 'http://your-server-address/tts'
data = {'text': 'Hello, world! This is a test.'}
response = requests.post(url, json=data)

# Save the audio file
with open('output.mp3', 'wb') as f:
    f.write(response.content)