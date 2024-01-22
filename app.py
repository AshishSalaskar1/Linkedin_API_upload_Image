from fastapi import FastAPI, Form, Header, Depends
import uvicorn
import requests
import logging


app = FastAPI()
logging.basicConfig(level=logging.INFO)



def upload_image_to_linkedin(oauth_token, upload_url, image_content, content_type):

    url = upload_url

    payload = image_content
    headers = {
        'Authorization': f'Bearer {oauth_token}',
        'Content-Type': content_type    
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    logging.info(f"LINKEDIN UPLOAD {response.text} WITH REPONSE CODE: {response.status_code}")
    return response.status_code


def getImageData(image_url):
    image_url = f"https:{image_url}"
    response = requests.get(image_url)

    logging.info(f"{image_url} -> RESPONSE : {response.content}")

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        image_data = response.content
        return image_data


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
    img_content = getImageData(form_data["contentUrl"])

    response_code = upload_image_to_linkedin(
        oauth_token = headers["Authorization"], 
        upload_url = headers["Upload_Url"], 
        image_content = img_content, 
        content_type = headers["Content_Type"]
    )

    return {
        "result":"SUCCESS", 
        "responseCode": response_code ,
        "formData": form_data, 
        "headers": headers,
        # "imgContent": img_content,
        "imgContentType": type(img_content)
    }



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8032)