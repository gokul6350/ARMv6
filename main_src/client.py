import cv2
import numpy as np
import requests
import base64
from dotenv import dotenv_values
env_values = dotenv_values()





def handshake():

    url = env_values['vision_server']

   
    

    try:
        response = requests.get(url)
        if response.status_code == 200:

            data = response.json()

    
            base64_data = data["base64"]
            image_data = base64.b64decode(base64_data)

            nparr = np.frombuffer(image_data, np.uint8)

            frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
           # print(data["objects"],data["origin"])
    
            return data["objects"],data["origin"],frame

        
    except Exception as e:
        #print(e)
        return None,None,None
    
