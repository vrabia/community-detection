import os

import requests
import load_env
from utils.plot import map_users


def upload_html(image_path, url='http://localhost:43614/vr-media/image/store-html'):
    with open(image_path, 'r') as file:
        html_content = file.read()

    client_id = os.getenv("PYTHON_CLIENT_ID")
    headers = {'Client-Id': client_id}

    url = url + "?filename=" + image_path.split("/")[-1]

    response = requests.post(url, data=html_content, headers=headers)
    return response


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


def save_image_and_upload_html(image_name, communities, colors):
    map_users(image_name, communities, colors)

    response = upload_image("images/" + image_name + ".png")

    if response.ok:
        print("Image ", image_name, "  uploaded successfully.")
        response = upload_html("html/" + image_name + ".html")
        if response.ok:
            print("HTML for ", image_name, " uploaded successfully.")
        else:
            print("Error uploading HTML ", image_name, ": ", response.status_code)
    else:
        print("Error uploading image ", image_name, ": ", response.status_code)
