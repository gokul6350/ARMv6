#!pip install elevenlabs

	
from elevenlabs import play , save
from elevenlabs.client import ElevenLabs
import uuid

client = ElevenLabs(
  api_key="", # Defaults to ELEVEN_API_KEY
)

audio = client.generate(
  text="",
  voice="Josh",
  model="eleven_multilingual_v2"
)
play(audio)
save(audio,uuid.uuid4())