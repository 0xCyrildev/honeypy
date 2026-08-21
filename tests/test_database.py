from honeypy.core.database import Database
from honeypy.models.attack import AttackEvent


def test_record_attack(tmp_path):
    database_path = tmp_path / "test.db"

    database = Database(str(database_path))

    event = AttackEvent(
        source_ip="127.0.0.1",
        event_type="ssh_login_attempt",
        username="root",
        password="toor",
    )

    database.record_attack(event)

    attacks = database.get_recent_attacks()

    assert len(attacks) == 1
    assert attacks[0][1] == "127.0.0.1"
    assert attacks[0][3] == "root"

    database.close()
