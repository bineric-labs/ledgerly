"""Storage: one in-memory SQLite database for the life of the process, seeded with two teams."""
import sqlite3
import threading

SEED = """
CREATE TABLE users(id INTEGER PRIMARY KEY, email TEXT, name TEXT, team_id INTEGER, is_admin INTEGER DEFAULT 0);
CREATE TABLE invoices(id INTEGER PRIMARY KEY, team_id INTEGER, customer TEXT, amount_nok INTEGER, status TEXT);
INSERT INTO users(id, email, name, team_id, is_admin) VALUES
  (1, 'ingrid@fjordbyra.no', 'Ingrid', 1, 1),
  (2, 'lars@fjordbyra.no',   'Lars',   1, 0),
  (3, 'sofie@nordlys.no',    'Sofie',  2, 0);
INSERT INTO invoices(id, team_id, customer, amount_nok, status) VALUES
  (1, 1, 'Bergen Kaffe AS',    12500, 'sent'),
  (2, 1, 'Tromso Sykkel',       4800, 'paid'),
  (3, 2, 'Oslo Arkitekter',    98000, 'draft'),
  (4, 2, 'Stavanger Energi',  240000, 'sent');
"""

_conn = None
_lock = threading.Lock()


def get_db() -> sqlite3.Connection:
    global _conn
    with _lock:
        if _conn is None:
            _conn = sqlite3.connect(":memory:", check_same_thread=False, isolation_level=None)
            _conn.row_factory = sqlite3.Row
            _conn.executescript(SEED)
    return _conn
