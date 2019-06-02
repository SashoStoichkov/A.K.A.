import sqlite3
from const import STUB_NAME, CREATE_STUB_SCRIPT, PURGE_STUB_SCRIPT


class StubManager:
    def __init__(self):
        self.conn = sqlite3.connect(STUB_NAME)

    def __enter__(self):
        self.conn.executescript(CREATE_STUB_SCRIPT)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.executescript(PURGE_STUB_SCRIPT)
        self.conn.close()

    
    
    @staticmethod
    def purge_stub(conn):
        conn.executescript(PURGE_STUB_SCRIPT)




