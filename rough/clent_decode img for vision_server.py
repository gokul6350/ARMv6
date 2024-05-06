import cv2
import numpy as np
import requests
import base64


url = "http://127.0.0.1:5000/dynamic_text"

response = requests.get(url)


if response.status_code == 200:

    data = response.json()

    # Decode the base64-encoded image data
    base64_data = data["base64"]
    image_data = base64.b64decode(base64_data)

    # Convert the image data to a numpy array
    nparr = np.frombuffer(image_data, np.uint8)

    # Decode the image using OpenCV
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Display the image
    cv2.imshow("Image", frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

else:
    print("Failed to fetch data from the API")
