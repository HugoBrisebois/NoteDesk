import sqlite3
from datetime import datetime, timedelta

class TimerStats:
    def __init__(self):
        self.db_file = "timer_stats.db"
        self.conn = sqlite3.connect(self.db_file)
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS timer_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                duration INTEGER, -- duration in seconds
                task_id INTEGER,
                completed BOOLEAN DEFAULT 1
            )
        ''')
        self.conn.commit()

    def record_session(self, duration, task_id=None, completed=True):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO timer_sessions (duration, task_id, completed)
            VALUES (?, ?, ?)
        ''', (duration, task_id, completed))
        self.conn.commit()

    def get_daily_stats(self, date=None):
        if date is None:
            date = datetime.now().date()

        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT SUM(duration), COUNT(*) 
            FROM timer_sessions 
            WHERE date(start_time) = date(?)
            AND completed = 1
        ''', (date.isoformat(),))
        
        total_duration, completed_sessions = cursor.fetchone()
        return {
            'total_duration': timedelta(seconds=total_duration or 0),
            'completed_sessions': completed_sessions or 0
        }

    def get_task_stats(self, task_id):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT SUM(duration), COUNT(*) 
            FROM timer_sessions 
            WHERE task_id = ? 
            AND completed = 1
        ''', (task_id,))
        
        total_duration, completed_sessions = cursor.fetchone()
        return {
            'total_duration': timedelta(seconds=total_duration or 0),
            'completed_sessions': completed_sessions or 0
        }
