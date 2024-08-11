import cv2
import numpy as np
from io import BytesIO
from PIL import Image
import base64

def process_image(img: np.ndarray) -> np.ndarray:
    # Convert the image to the HSV color space
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Define a range of blue color in the HSV color space
    lower_blue = np.array([110, 50, 50])
    upper_blue = np.array([130, 255, 255])

    # Create a binary mask
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # Apply the binary mask to the image
    sky = cv2.bitwise_and(img, img, mask=mask)

    # Find the coordinates of the square
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        cnt = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(cnt)

        # Create the rectangular ROI
        roi = sky[y:y+h, x:x+w]
        return roi
    else:
        # Return the original image if no blue sky is detected
        return img

def image_to_base64(img: np.ndarray) -> str:
    _, buffer = cv2.imencode('.jpg', img)
    img_base64 = base64.b64encode(buffer).decode('utf-8')
    return img_base64