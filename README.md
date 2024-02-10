### Python API which acts like a wrapper for imageUpload API provided by Linkedin API

**Request Format**
- URL: https://ash-inkedin-api-upload-image.vercel.app/uploadImage
- METHOD: POST
- Headers:
    - `Authorization`: `<OAuth_Bearer_Token>`
    - `Upload-Url`: Linkedin Upload URL obtained after hitting `/registerUpload`
    - `Content-Type`: Image Type
- Body (form_data)
    - `contentUrl`: <web url of the image resource>

**Response Format**    
```json
{
  "result":"SUCCESS",
  "responseCode":201,
  "formData":{
      "contentUrl":"//ff22307d23eb9d2dd90f452e2e1d6f9.cdn.bubble.io/f1705957170658x141430425408167310/fake_note.png"},
       "headers":{
            "Authorization":"Bearer xxxxxx",
            "Upload_Url":"https://api.linkedin.com/mediaUpload/ut=2v_",
            "Content_Type":"multipart/form-data"
        }
}
```
