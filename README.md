# **ARMv7**

### Tools & Software Used

- **TTS:** ElevenLabs
- **Object Detection:** YOLOv8 by Ultralytics
- **Vision Annotation** Roboflow
- **Speech to Text:** Wisper AI
- **LLM:** Google Gemini Pro
- **Microcontroller:** Arduino Uno
- **UI:** Gradio
- **2D Simulator:** Matplotlib
- **Code Language:** Python 3.10.3

If you have $$$ for GPUs (not recommended), then you can make it completely offline.

### LLM Part:

- You can fine-tune a Mistral 7B with your data.
  - **Model:** [Mistral-7B-v0.1](https://huggingface.co/mistralai/Mistral-7B-v0.1/discussions/133)
  - **Tutorial:** [Mistral-7B Tutorial](https://www.datacamp.com/tutorial/mistral-7b-tutorial)
- My model (LORA Adapter Model) (FLOP): [Loara Chat Arm](https://huggingface.co/gokul00060/loara-chat-arm/tree/main)

### Speech to Text:

- You can run the same Wisper model locally with minor changes.

### TTS:

- In the text-to-speech model, you can use Bark. I tried Bark for this project. In Bark, you can even clone your voice.
  - [Bark GitHub Repository](https://github.com/suno-ai/bark)
