import os
import requests

class InstagramService:
    def __init__(self):
        self.access_token = os.getenv('INSTAGRAM_ACCESS_TOKEN')
        self.api_url = "https://graph.facebook.com/v18.0"
    
    def send_message(self, recipient_id: str, message: str):
        url = f"{self.api_url}/me/messages"
        payload = {
            "recipient": {"id": recipient_id},
            "message": {"text": message},
            "access_token": self.access_token
        }
        requests.post(url, json=payload)
    
    def send_attachment(self, recipient_id: str, attachment_url: str, message: str):
        url = f"{self.api_url}/me/messages"
        payload = {
            "recipient": {"id": recipient_id},
            "message": {
                "attachment": {
                    "type": "file",
                    "payload": {"url": attachment_url}
                }
            },
            "access_token": self.access_token
        }
        requests.post(url, json=payload)
        if message:
            self.send_message(recipient_id, message)
    
    def verify_webhook(self, mode: str, token: str, challenge: str) -> str:
        verify_token = os.getenv('INSTAGRAM_VERIFY_TOKEN')
        if mode == "subscribe" and token == verify_token:
            return challenge
        return "Verification failed"
