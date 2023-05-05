import os

import requests
import load_env


def upload_image(image_path, url='http://localhost:43614/vr-media/image/communities'):
    # Open the image file
    image_file = open(image_path, "rb")

    # Create a dictionary with the image file and key "file"
    files = {"file": image_file}

    client_id = os.getenv("PYTHON_CLIENT_ID")
    headers = {'Client-Id': client_id}

    # Send a POST request with the image file as the body
    response = requests.post(url, files=files, headers=headers)

    # Close the image file
    image_file.close()

    # Return the response
    return response
