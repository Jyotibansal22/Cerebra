import sqlite3
from datetime import datetime

def connect_db():
    conn = sqlite3.connect("cerebra.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            content TEXT,
            tag TEXT,
            date TEXT
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT,
            done INTEGER,
            tag TEXT,
            date TEXT
        )
    """)
    conn.commit()
    conn.close()

# Notes
def add_note(title, content, tag):
    conn = sqlite3.connect("cerebra.db")
    c = conn.cursor()
    c.execute("INSERT INTO notes (title, content, tag, date) VALUES (?, ?, ?, ?)",
              (title, content, tag, datetime.now().strftime("%Y-%m-%d %H:%M")))
    conn.commit()
    conn.close()

def get_notes(search_query="", tag_filter=""):
    conn = sqlite3.connect("cerebra.db")
    c = conn.cursor()
    query = "SELECT * FROM notes WHERE title LIKE ?"
    values = (f"%{search_query}%",)
    if tag_filter:
        query += " AND tag=?"
        values += (tag_filter,)
    c.execute(query, values)
    data = c.fetchall()
    conn.close()
    return data

def delete_note(note_id):
    conn = sqlite3.connect("cerebra.db")
    c = conn.cursor()
    c.execute("DELETE FROM notes WHERE id=?", (note_id,))
    conn.commit()
    conn.close()

# Tasks
def add_task(task, tag=""):
    conn = sqlite3.connect("cerebra.db")
    c = conn.cursor()
    c.execute("INSERT INTO tasks (task, done, tag, date) VALUES (?, ?, ?, ?)",
              (task, 0, tag, datetime.now().strftime("%Y-%m-%d %H:%M")))
    conn.commit()
    conn.close()

def get_tasks(search_query="", tag_filter=""):
    conn = sqlite3.connect("cerebra.db")
    c = conn.cursor()
    query = "SELECT * FROM tasks WHERE task LIKE ?"
    values = (f"%{search_query}%",)
    if tag_filter:
        query += " AND tag=?"
        values += (tag_filter,)
    c.execute(query, values)
    data = c.fetchall()
    conn.close()
    return data

def delete_task(task_id):
    conn = sqlite3.connect("cerebra.db")
    c = conn.cursor()
    c.execute("DELETE FROM tasks WHERE id=?", (task_id,))
    conn.commit()
    conn.close()

def toggle_task(task_id, status):
    conn = sqlite3.connect("cerebra.db")
    c = conn.cursor()
    c.execute("UPDATE tasks SET done=? WHERE id=?", (1 - status, task_id))
    conn.commit()
    conn.close()
