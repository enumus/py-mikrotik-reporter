import configparser
import os

import paramiko


class MtConnector:
    """Mikrotik command execution class"""
    def __init__(self):
        cfg = configparser.ConfigParser()
        cfg.read('/app/config.ini')

        # Setting configuration values
        self.mt_gateway = cfg.get('Mikrotik', 'gateway', vars=os.environ)
        self.mt_user = cfg.get('Mikrotik', 'user', vars=os.environ)
        self.mt_password = cfg.get('Mikrotik', 'password', vars=os.environ)

        self.conn = paramiko.SSHClient()
        self.conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.conn.connect(
            self.mt_gateway,
            username=self.mt_user,
            password=self.mt_password,
            allow_agent=False,
            look_for_keys=False
        )

    def add_to_blacklist(self, ip):
        cmd = f"/ip firewall address-list add list=blacklist address={ip}/32"
        stdin, stdout, stderr = self.conn.exec_command(cmd)
        if stdout.readline() == "":
            return True
        else:
            return False

    def send_command(self, cmd):
        stdin, stdout, stderr = self.conn.exec_command(cmd)

        return stdout

    def close_connection(self):
        self.conn.close()

