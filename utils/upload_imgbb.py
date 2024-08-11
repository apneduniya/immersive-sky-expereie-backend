import requests
import os


def upload_image_to_imgbb(base64_image: str) -> dict:
    print("Uploading image to ImgBB")

    # URL to the ImgBB API with the API key
    url = f"https://api.imgbb.com/1/upload?key={
        os.getenv('NEXT_PUBLIC_IMGBB_API_KEY')}"

    # Prepare the form data
    form_data = {
        "image": base64_image
    }

    try:
        # Make the POST request to upload the image
        response = requests.post(url, data=form_data)

        # Check if the response is successful
        if response.status_code != 200:
            raise Exception(f"HTTP error! Status: {response.status_code}")

        # Parse the response JSON
        data = response.json()

        return data
    except Exception as error:
        print(f'Error uploading image: {error}')
        raise error
