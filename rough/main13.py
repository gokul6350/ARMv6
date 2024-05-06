import json
import chat
from rich import print
import gradio as gr
import datetime
from log import log1
from elevenlabs import play , save
from elevenlabs.client import ElevenLabs
import uuid


#chat = Chat(system="You are a helpful assistant.")

client = ElevenLabs(api_key="",)
def run_text_prompt(message, chat_history):
   
    rep=chat.gen_ai(message)
 #   discord2.post(content=f"{rep}")
    log1(f"RESPONCES FOR LLM: {rep}")
    audio = client.generate(
        text=rep,
        voice="Josh",
        model="eleven_multilingual_v2"
    )

    play(audio)

    chat_history.append((message, rep))
    return "", chat_history


def run_audio_prompt(audio, chat_history):
    if audio is None:
        return None, chat_history

   # message_transcription = model.transcribe(audio)["text"]
   # _, chat_history = run_text_prompt(message_transcription, chat_history)
    log1("TRANS NOT ADDED")
    return None, chat_history


with gr.Blocks(theme=gr.themes.Soft) as demo:
    chatbot = gr.Chatbot(height=650)

    msg = gr.Textbox()
    msg.submit(run_text_prompt, [msg, chatbot], [msg, chatbot])
    chatbot.change()
    with gr.Row():
        audio = gr.Audio(sources="microphone", type="filepath")
        
        send_audio_button = gr.Button("Send Audio", interactive=True)
        send_audio_button.click(run_audio_prompt, [audio, chatbot], [audio, chatbot])

demo.launch(debug=True,favicon_path="icon.png")
     