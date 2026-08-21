"""
HoneyPy entry point.
"""

from honeypy.config import HOST, SSH_PORT, SERVER_NAME, VERSION
from honeypy.core.database import Database
from honeypy.core.events import EventProcessor
from honeypy.services.ssh import SSHHoneypot


def main():
    print()
    print("=" * 50)
    print(f"{SERVER_NAME} v{VERSION}")
    print("Adaptive Python Honeypot")
    print("=" * 50)
    print()

    database = Database()
    event_processor = EventProcessor(database)

    ssh_honeypot = SSHHoneypot(
        host=HOST,
        port=SSH_PORT,
        event_processor=event_processor,
    )

    try:
        ssh_honeypot.start()
    except KeyboardInterrupt:
        print("\n[!] HoneyPy shutting down...")
    finally:
        database.close()


if __name__ == "__main__":
    main()
