#!/usr/bin/python
import sys
sys.path.append("/app/connectors")

from mikrotik_connector import MtConnector

try:
    mt_conn = MtConnector()
    ip = input("IP: ")

    if ip == "":
        command = "/ip firewall address-list remove [find where list=blacklist]"
    else:
        command = f"/ip firewall address-list remove [find where address={ip}]"

    output = mt_conn.send_command(command)
    if output == "":
        print("IP(s) deleted successfully from blacklist")
    else:
        for line in output:
            print(line.strip("\n"))

    # Add back Censys.io IP range when clearing the blacklist
    if ip == "":
        command = "/ip firewall address-list add list=blacklist address=162.142.125.0/24"

    output = mt_conn.send_command(command)
    if output == "":
        print("Censys.io IP range is back on the list")
    else:
        for line in output:
            print(line.strip("\n"))

    mt_conn.close_connection()
except Exception as e:
    print(f"Oh oh... Some kind of error happened. Error: {e}")
