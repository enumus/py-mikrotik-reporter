import configparser
import os
import requests


class AbuseIPDBConnector:
    """Abuse IP DB API connection class"""
    def __init__(self):
        cfg = configparser.ConfigParser()
        cfg.read('config.ini')

        # Setting configuration values
        self.abuse_endpoint = cfg.get('AbuseIPDB', 'endpoint', vars=os.environ)
        self.abuse_key = cfg.get('AbuseIPDB', 'key', vars=os.environ)
        self.base_url = "https://api.abuseipdb.com"

    def report(self, ip, *args, **kwargs):
        port = kwargs.get("port", None)
        comment = f"Unauthorised connection attempt from IP {ip}"
        if port:
            comment = comment + f" Port {port}"

        url = f"{self.base_url}{self.abuse_endpoint}"
        data = {
            'ip': ip,
            'categories': '14,15,18',
            'comment': comment
        }

        headers = {
            'Key': self.abuse_key
        }

        try:
            r = requests.post(url, json=data, headers=headers)
            r.raise_for_status()
            return r.json()
        except requests.exceptions.HTTPError as err:
            raise Exception(err)
