import os
import sqlite3 as sql

DATABASE_URL = os.getenv('dbinfo', "main.db")


class Database:
    def __init__(self):
        self.connection = sql.connect(DATABASE_URL, timeout=20, check_same_thread=False)
        self.connection.row_factory = sql.Row
        self.cursor = self.connection.cursor()
        self._ensure_tables_exist()

    def _table_exists(self, table_name):
        self.cursor.execute("select count(*) from sqlite_master where type='table' and name=?", (table_name,))
        result = self.cursor.fetchall()
        result = (result[0][0])
        return result > 0

    def _ensure_tables_exist(self):
        self._ensure_table_exists('settings', """
            name TEXT UNIQUE,
            value TEXT
        """)
        self._ensure_table_exists('tasks', """
            id TEXT,
            task_type TEXT,
            filename TEXT,
            rdstatus TEXT,
            rdprogressdownload INTEGER,
            attemptstogetlink INTEGER,
            rderror TEXT,
            completed TEXT,
            Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        """)

    def _ensure_table_exists(self, table_name, columns):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS {} ({})".format(table_name, columns))
        self.connection.commit()

    def update_setting(self, setting_name, setting_value):
        self.cursor.execute("""
            INSERT INTO settings(name, value) VALUES(?, ?)
            ON CONFLICT(name) DO UPDATE SET value=?""", (setting_name, setting_value, setting_value))
        self.connection.commit()

    def get_all_settings(self):
        self.cursor.execute("SELECT * FROM settings")
        result = self.cursor.fetchall()
        if len(result) == 0:
            self.update_setting('waitbetween', '300')
            self.update_setting('maxattempts', '10')
            self.update_setting('aria2host', 'http://0.0.0.0')
            self.update_setting('rdapikey', 'placeholderapikey')
            self.update_setting('username', 'admin')
            self.update_setting('password', 'admin')
            self.cursor.execute("SELECT * FROM settings")
            result = self.cursor.fetchall()

        settings_dict = {
            res['name']: res['value'] for res in result
        }
        return settings_dict

    def get_tasks(self):
        self.cursor.execute("SELECT * FROM tasks ORDER BY Timestamp DESC")
        result = self.cursor.fetchall()
        tasks = [
            {k: r[k] for k in r.keys()}
            for r in result
        ]
        return tasks

    def get_task(self, task_id):
        self.cursor.execute("SELECT * FROM tasks WHERE id=?", (task_id,))
        result = self.cursor.fetchone()
        if len(result) == 0:
            return None
        return {k: result[k] for k in result.keys()}

    def update_task(self, task_id, field, value):
        self.cursor.execute("UPDATE tasks SET {}=? WHERE id=?".format(field), (value, task_id))
        self.connection.commit()

    def add_task(self, myid,
                 task_type,
                 name,
                 status,
                 progress,
                 attempts,
                 rderror,
                 completed):
        res = self.cursor.execute(
            """INSERT INTO 
            tasks(id, task_type, filename, rdstatus, rdprogressdownload, attemptstogetlink ,rderror,completed) 
            VALUES (?,?,?,?,?,?,?,?)""",
            (myid, task_type, name, status, progress, attempts, rderror, completed))
        self.connection.commit()

    def delete_task(self, task_id):
        self.cursor.execute("DELETE FROM tasks WHERE id=?", (task_id,))
        self.connection.commit()

    def delete_all_tasks(self):
        self.cursor.execute("DELETE FROM tasks")
        self.connection.commit()


database = Database()
