# db.py
import sqlite3
import json
from typing import List

DB_PATH = "legal_cases.db"

def get_conn():
    conn = sqlite3.connect(DB_PATH, timeout=30)
    return conn

def init_db():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS cases (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        case_name TEXT UNIQUE,
        year INTEGER,
        file_path TEXT,
        entities TEXT
                
    )
    """)
    conn.commit()
    conn.close()

def store_case(case_name: str, year: int, file_path: str, entities: List[str]):
    conn = get_conn()
    cur = conn.cursor()
    entities_json = json.dumps(entities, ensure_ascii=False)
    try:
        cur.execute("""
            INSERT INTO cases (case_name, year, file_path, entities)
            VALUES (?, ?, ?, ?)
        """, (case_name, year, file_path, entities_json))
        conn.commit()
    except sqlite3.IntegrityError:
        # already exists, skip
        pass
    finally:
        conn.close()

def case_exists(case_name: str) -> bool:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM cases WHERE case_name = ? LIMIT 1", (case_name,))
    res = cur.fetchone()
    conn.close()
    return res is not None

def fetch_all_cases():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, case_name, year, file_path, entities FROM cases")
    rows = cur.fetchall()
    conn.close()
    # parse entities JSON
    import json
    cases = []
    for r in rows:
        cases.append({
            "id": r[0],
            "case_name": r[1],
            "year": r[2],
            "file_path": r[3],
            "entities": json.loads(r[4])
        })
    return cases
