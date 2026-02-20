import os
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse

class WhatsAppService:
    def __init__(self):
        self.client = Client(
            os.getenv('TWILIO_ACCOUNT_SID'),
            os.getenv('TWILIO_AUTH_TOKEN')
        )
        self.from_number = os.getenv('TWILIO_WHATSAPP_NUMBER')
    
    def send_message(self, to_number: str, message: str):
        self.client.messages.create(
            from_=self.from_number,
            body=message,
            to=to_number
        )
    
    def send_pdf(self, to_number: str, pdf_url: str, message: str):
        self.client.messages.create(
            from_=self.from_number,
            body=message,
            media_url=[pdf_url],
            to=to_number
        )
    
    def create_response(self, message: str) -> str:
        response = MessagingResponse()
        response.message(message)
        return str(response)
