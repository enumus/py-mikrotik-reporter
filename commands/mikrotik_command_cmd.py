#!/usr/bin/python
import connectors.mikrotik_connector as mc

mt_conn = mc.MtConnector()
command = input("Mikrotik command: ")

output = mt_conn.send_command(command)
print("Mikrotik response:")
for line in output:
    print(line.strip("\n"))

mt_conn.close_connection()
