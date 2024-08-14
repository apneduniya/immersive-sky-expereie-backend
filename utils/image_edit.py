import cv2
import numpy as np
from io import BytesIO
from PIL import Image
import base64

def process_image(img: np.ndarray) -> np.ndarray:
    # Get the dimensions of the image
    height, width, _ = img.shape

    # Define the cropping region (top 30% of the image)
    crop_height = int(height * 0.3)  # Adjust 0.3 to increase or decrease the crop

    # Crop the top part of the image
    sky = img[:crop_height, :]
    sky = cv2.cvtColor(sky, cv2.COLOR_BGR2RGB)

    # # Find the coordinates of the square
    # contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # if contours:
    #     cnt = max(contours, key=cv2.contourArea)
    #     x, y, w, h = cv2.boundingRect(cnt)

    #     # Create the rectangular ROI
    #     roi = sky[y:y+h, x:x+w]
    #     return roi
    # else:
    #     # Return the original image if no blue sky is detected
    #     return img

    return sky

def image_to_base64(img: np.ndarray) -> str:
    _, buffer = cv2.imencode('.jpg', img)
    img_base64 = base64.b64encode(buffer).decode('utf-8')
    return img_base64