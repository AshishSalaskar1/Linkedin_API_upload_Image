from fastapi import FastAPI, Form, Header, Depends
import uvicorn

app = FastAPI()


async def upload_image():
  return { 
    "message": "Welcome to my notes application, use the /docs route to proceed"
   }

# Dependency to get headers
def get_headers(Authorization: str = Header(...)):
    return {"Authorization": Authorization}

# Dependency to get form data
def get_form_data(content: str = Form(...)):
    print(content);
    print(type(content));
    return {"content": content}


@app.post("/uploadImage")
async def process_data(
    form_data: dict = Depends(get_form_data),
    headers: dict = Depends(get_headers)
):
    return {"form_data": form_data, "headers": headers}



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8032)