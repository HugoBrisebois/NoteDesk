import sqlite3
from datetime import datetime

class NotesDatabase:
    def __init__(self):
        self.db_file = "notes/notes.db"
        self.conn = sqlite3.connect(self.db_file)
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()

    def add_note(self, title, content, category=None, task_id=None):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO notes (title, content)
            VALUES (?, ?)
        ''', (title, content))
        self.conn.commit()
        return cursor.lastrowid

    def get_all_notes(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM notes ORDER BY created_at DESC')
        return cursor.fetchall()

    def get_note(self, note_id):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM notes WHERE id = ?', (note_id,))
        return cursor.fetchone()

    def update_note(self, note_id, title, content):
        cursor = self.conn.cursor()
        cursor.execute('''
            UPDATE notes 
            SET title = ?, content = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (title, content, note_id))
        self.conn.commit()

    def delete_note(self, note_id):
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM notes WHERE id = ?', (note_id,))
        self.conn.commit()

    def __del__(self):
        self.conn.close()