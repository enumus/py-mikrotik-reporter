import configparser
import re
import json
import os

from flask import Blueprint, request, abort
from connectors.mikrotik_connector import MtConnector
from connectors.abuseipdb_connector import AbuseIPDBConnector
from connectors.telegram_connector import TelegramConnector

api_reporter = Blueprint("api_reporter", __name__, url_prefix="/api/report")

cfg = configparser.ConfigParser()
cfg.read('config.ini')

# Setting configuration values
active_tokens = json.loads(cfg.get('System', 'active_tokens', vars=os.environ))
authorised_users = json.loads(cfg.get('System', 'authorised', vars=os.environ))

# create a global telegram connector
# tg_conn = TelegramConnector()


def get_ip_from_message(message):
    ips = re.findall(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", message)
    ip = ips[len(ips)-1]

    return ip


def get_port_from_message(message):
    ports = re.findall(r"\[\d*]", message)
    if len(ports) > 0:
        port = ports[len(ports)-1]
        return port[1:-1]
    else:
        return


def find_source(message):
    source = re.search(r"\[[A-Za-z\-_]*]", message)
    return source.group()


def find_time(message):
    time = re.search(r"[A-Za-z]{0,3}\S?[0-9]{0,2}\s*\d{1,2}:\d{1,2}:\d{1,2}", message)
    if time:
        return time.group()
    else:
        return


def process_message(message):
    ip = get_ip_from_message(message)
    port = get_port_from_message(message)

    # Adds the ip to Mikrotiks blacklist and sends a notification to Telegram
    mt_conn = MtConnector()
    mt_res = mt_conn.add_to_blacklist(ip=ip)
    if mt_res:
        # tg_conn.send(message=f"IP {ip} has been added to the blacklist successfully")
    else:
        # tg_conn.send(message=f"It has been an error when adding the IP {ip} to the blacklist")
    mt_conn.close_connection()

    # Reports the IP to Abuse IP DB and sends a notification to Telegram
    # ab_conn = AbuseIPDBConnector()
    # if port:
    #     print("Port:", port)
    #     ab_res = ab_conn.report(ip=ip, port=port)
    # else:
    #     ab_res = ab_conn.report(ip=ip)
    # if "error" in ab_res:
    #     tg_conn.send(message=f"It has been an error when reporting the IP {ip}. Error: {ab_res['errors'][0]['detail']}")
    # else:
    #     tg_conn.send(message=f"IP {ip} has been reported successfully. Score: {ab_res['data']['abuseConfidenceScore']}")


def process_data(data):
    message = data['message']

    if any(authorised_user in message for authorised_user in authorised_users):
        print("Skipping process")
        return

    # tg_conn.send(message=message)
    print("This is the message:", message)

    source = find_source(message)
    time = find_time(message)
    process_message(message)


@api_reporter.route('/messages/<token>', methods=['POST'])
def get_messages(token):
    if request.method == 'POST':
        if token not in active_tokens:
            print("The token does not match")
            abort(401)

        try:
            process_data(request.json)
            return 'success', 200
        except Exception as e:
            # tg_conn.send(message=str(e))
            abort(500)
    else:
        print("The call is not a POST call")

        abort(400)
