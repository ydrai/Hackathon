# aws_client.py
from boto3.session import Session
from config import load_config
import uuid

class AWSClient:
    def __init__(self, session_id=None):
        self.config = load_config()['Lex']
        self.client = self.create_client()
        self.session_id = session_id if session_id else str(uuid.uuid4())

    def create_client(self):
        session = Session(
            aws_access_key_id=self.config['aws_access_key_id'],
            aws_secret_access_key=self.config['aws_secret_access_key'],
            region_name=self.config['region_name'],
        )
        return session.client('lexv2-runtime')

    def send_message(self, text):
        response = self.client.recognize_text(
            botId=self.config['bot_id'],
            botAliasId=self.config['bot_alias_id'],
            localeId=self.config['locale_id'],
            sessionId=self.session_id,  # Utiliser l'UUID généré
            text=text
        )
        return response['messages'][0]['content']
