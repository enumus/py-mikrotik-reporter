import configparser
import os
import requests


class TelegramConnector:
    """Telegram API connection class"""
    def __init__(self):
        cfg = configparser.ConfigParser()
        cfg.read('/app/config.ini')

        # Setting configuration values
        self.tg_token = cfg.get('Telegram', 'token', vars=os.environ)
        self.tg_chat_id = cfg.get('Telegram', 'chat_id', vars=os.environ)
        self.base_url = f"https://api.telegram.org/bot{self.tg_token}"

    def send(self, message):
        data = {
            "chat_id": self.tg_chat_id,
            "text": message
        }

        url = f"{self.base_url}/sendMessage"

        try:
            r = requests.post(url, json=data)
            r.raise_for_status()
            return True
        except requests.exceptions.HTTPError as err:
            # TODO log the error
            raise Exception(err)
