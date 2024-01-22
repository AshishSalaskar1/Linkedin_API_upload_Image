import requests

# URL of the image file
image_url = "https://ff22307d2e3eb9d2dd90f452e2e1d6f9.cdn.bubble.io/f1705957170658x141430425408167310/fake_note.png"

# Make a request to the URL to get the image data
response = requests.get(image_url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Access the content of the response, which contains the image data as bytes
    image_data = response.content
    print(image_data)

    # # Process the image_data as needed
    # # For example, you can save it to a file
    # with open("fake_note.png", "wb") as image_file:
    #     image_file.write(image_data)

else:
    print(f"Failed to fetch the image. Status code: {response.status_code}")