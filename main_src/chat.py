
import google.generativeai as genai
from dotenv import dotenv_values






# Load environment variables from .env file
env_vars = dotenv_values()
#genai.configure(api_key=env_vars["google_key"])

# Set up the model
generation_config = {
  "temperature": 0.9,
  "top_p": 1,
  "top_k": 0,
  "max_output_tokens": 8192,
}

safety_settings = [
]

model = genai.GenerativeModel(model_name="tunedModels/dataset-reb3qi4cuvqu",
                              generation_config=generation_config,
                              safety_settings=safety_settings)
def gen_ai(prompt):
    prompt_parts = [
    "input: pickup battery",
    "output: _pickup(battery) #picking up the batter",
    "input: what is the distance between moon and earth",
    "output: distance between moon and earth is 384,400 km  ",
    f"input: {prompt}",
    "output: ",
    ]

    response = model.generate_content(prompt_parts)
    print(f">>>{response.text}")
    
    return response.text
