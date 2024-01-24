from fastapi import FastAPI, Form, Header, Depends
import uvicorn
import requests
import logging
import mimetypes
import os
from datetime import datetime

app = FastAPI()
logging.basicConfig(level=logging.ERROR)

def update_local_logs(img_url):
    if not os.path.exists("li_logs.txt"):
        with open("/tmp/li_logs.txt","w") as f:
            f.write(f"IMAGE_URL | TIMESTAMP\n")

    timestamp = str(datetime.now())
    with open("/tmp/li_logs.txt","a") as f:
        f.write(f"{img_url} | {timestamp}\n")


def read_image(image_path):
    with open(image_path, 'rb') as file:
        content_type, _ = mimetypes.guess_type(image_path)
        # image_base64 = base64.b64encode(file.read()).decode('utf-8')

        return file.read(), content_type
    
def upload_image_to_linkedin(oauth_token, upload_url, image_path):

    url = upload_url
    img_content, content_type = read_image(image_path)

    payload = img_content
    headers = {
        'Authorization': f'{oauth_token}',
        'Content-Type': content_type    
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print("TEXT",response.text,"CODE:",response.status_code)
    return response.status_code

def getImageData(image_url):
    image_url = f"https:{image_url}"
    local_filename = f"/tmp/img.{image_url.split('.')[-1]}"
    response = requests.get(image_url)

    logging.error(image_url)
    # logging.info(f"{image_url} -> RESPONSE : {response.content}")

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        with open(local_filename, 'wb') as file:
            file.write(response.content)

        return local_filename
        # image_data = response.content
        # return image_data


# Dependency to get headers
def get_headers(
        Authorization: str = Header(...), 
        Upload_Url: str = Header(...),
        Content_Type: str = Header(...) 
    ):
    return {
        "Authorization": Authorization,
        "Upload_Url": Upload_Url,
        "Content_Type": Content_Type
    }

# Dependency to get form data
def get_form_data(contentUrl: str = Form(...)):
    return {"contentUrl": contentUrl}


@app.post("/uploadImage")
async def process_data(
    form_data: dict = Depends(get_form_data),
    headers: dict = Depends(get_headers)
):
    img_path = getImageData(form_data["contentUrl"])

    response_code = upload_image_to_linkedin(
        oauth_token = headers["Authorization"], 
        upload_url = headers["Upload_Url"], 
        image_path = img_path
    )

    update_local_logs(img_url=form_data["contentUrl"])

    return {
        "result":"SUCCESS", 
        "responseCode": response_code ,
        "formData": form_data, 
        "headers": headers
    }

@app.get("/metrics")
async def get_metrics():
    if not os.path.exists("li_logs.txt"):
        return {
            "logs": []
        }
    
    with open("/tmp/li_logs.txt") as f:
        logs = f.readlines()
    
    return {
        "logs": logs
    }

@app.get("/hello")
async def hello():
    return "HELLO FROM THIS API"


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8032)