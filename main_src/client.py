import cv2
import numpy as np
import requests
import base64


def handshake():

    url = "http://127.0.0.1:5000/dynamic_text"

   
    response = requests.get(url)


    if response.status_code == 200:

        data = response.json()

 
        base64_data = data["base64"]
        image_data = base64.b64decode(base64_data)

        nparr = np.frombuffer(image_data, np.uint8)

        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        print(data["objects"],data["origin"])
 
        return data["objects"],data["origin"],frame

    else:
        print("Failed to fetch data from the API")
