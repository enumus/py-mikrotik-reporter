#!/usr/bin/python
import sys
sys.path.append("/app/connectors")

from mikrotik_connector import MtConnector

try:
    mt_conn = MtConnector()
    command = input("Mikrotik command: ")

    output = mt_conn.send_command(command)
    print("Mikrotik response:")
    for line in output:
        print(line.strip("\n"))

    mt_conn.close_connection()
except Exception as e:
    print(f"It was some kind of an issue. Error: {e}")
