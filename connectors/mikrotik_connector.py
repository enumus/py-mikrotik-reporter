import configparser
import os

from pexpect import pxssh


class MtConnector:
    """Mikrotik command execution class"""
    def __init__(self):
        cfg = configparser.ConfigParser()
        cfg.read('config.ini')

        # Setting configuration values
        self.mt_gateway = cfg.get('Mikrotik', 'gateway', vars=os.environ)
        self.mt_user = cfg.get('Mikrotik', 'user', vars=os.environ)
        self.mt_password = cfg.get('Mikrotik', 'password', vars=os.environ)

        self.conn = pxssh.pxssh()
        self.conn.login(
            self.mt_gateway,
            username=self.mt_user,
            password=self.mt_password,
        )

    def add_to_blacklist(self, ip):
        cmd = f"/ip firewall address-list add list=blacklist address={ip}/32"
        r = self.send_command(cmd=cmd)
        if r == "":
            return True
        else:
            return False

    def send_command(self, cmd):
        self.conn.sendline(cmd)
        self.conn.prompt()
        return self.conn.before

    def close_connection(self):
        self.conn.logout()
