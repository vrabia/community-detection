from client.save_image import upload_image

response = upload_image("images/test.png")

if response.ok:
    print("Image uploaded successfully.")
else:
    print("Error uploading image:", response.status_code)
