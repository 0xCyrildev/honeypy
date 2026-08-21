"""
SSH honeypot service.

This service records authentication attempts.
It does not provide access to the underlying operating system.
"""

import socket
import threading

import paramiko

from honeypy.core.events import EventProcessor
from honeypy.models.attack import AttackEvent


class HoneySSHServer(paramiko.ServerInterface):
    def __init__(self, client_ip: str, event_processor: EventProcessor):
        self.client_ip = client_ip
        self.event_processor = event_processor

    def check_auth_password(self, username, password):
        event = AttackEvent(
            source_ip=self.client_ip,
            event_type="ssh_login_attempt",
            username=username,
            password=password,
        )

        self.event_processor.process(event)

        # Always reject authentication for now.
        return paramiko.AUTH_FAILED

    def get_allowed_auths(self, username):
        return "password"


class SSHHoneypot:
    def __init__(
        self,
        host: str,
        port: int,
        event_processor: EventProcessor,
    ):
        self.host = host
        self.port = port
        self.event_processor = event_processor

        self.host_key = paramiko.RSAKey.generate(2048)

    def start(self):
        sock = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )

        sock.setsockopt(
            socket.SOL_SOCKET,
            socket.SO_REUSEADDR,
            1
        )

        sock.bind((self.host, self.port))
        sock.listen(100)

        print(
            f"[+] HoneyPy SSH honeypot listening "
            f"on {self.host}:{self.port}"
        )

        while True:
            client, address = sock.accept()

            thread = threading.Thread(
                target=self._handle_client,
                args=(client, address),
                daemon=True,
            )

            thread.start()

    def _handle_client(self, client, address):
        client_ip = address[0]

        transport = None

        try:
            transport = paramiko.Transport(client)

            transport.add_server_key(self.host_key)

            server = HoneySSHServer(
                client_ip,
                self.event_processor,
            )

            transport.start_server(server=server)

            channel = transport.accept(10)

            if channel:
                channel.close()

        except Exception as error:
            print(
                f"[!] Connection error from "
                f"{client_ip}: {error}"
            )

        finally:
            if transport:
                transport.close()
