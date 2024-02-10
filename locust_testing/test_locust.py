from locust import HttpUser, task, between
import json

payload = {
    'contentUrl': '//ff22307d23eb9d2dd90f452e2e1d6f9.cdn.bubble.io/f1705957170658x141430425408167310/fake_note.png'
    }
headers = {
  'Authorization': 'Bearer <auth_token>',
  'Upload-Url': '<linkedin_upload_url>'
}


class ApiUser(HttpUser):
    wait_time = between(1, 2)  # wait time between requests in seconds

    @task(1)
    def post_data(self):
        self.client.post("/uploadImage", data=payload, headers=headers)
