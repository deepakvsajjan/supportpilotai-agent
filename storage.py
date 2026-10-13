import sqlite3, uuid
from pathlib import Path
from datetime import datetime, timezone
DB = Path(__file__).resolve().parent.parent / "data" / "support.db"
def connect():
    DB.parent.mkdir(exist_ok=True)
    c = sqlite3.connect(DB); c.row_factory = sqlite3.Row; return c
def init():
    with connect() as c:
        c.execute("CREATE TABLE IF NOT EXISTS messages(id INTEGER PRIMARY KEY, session_id TEXT, role TEXT, content TEXT, sources TEXT, created_at TEXT)")
        c.execute("CREATE TABLE IF NOT EXISTS feedback(id INTEGER PRIMARY KEY, session_id TEXT, message TEXT, rating INTEGER, comment TEXT, created_at TEXT)")
def save(session, role, text, sources=None):
    with connect() as c:
        c.execute("INSERT INTO messages(session_id,role,content,sources,created_at) VALUES(?,?,?,?,?)",(session,role,text,"; ".join(sources or []),datetime.now(timezone.utc).isoformat()))
def history(session):
    with connect() as c: rows=c.execute("SELECT role,content,sources,created_at FROM messages WHERE session_id=? ORDER BY id",(session,)).fetchall()
    return [dict(r) for r in rows]
