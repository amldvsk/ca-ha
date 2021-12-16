import sqlite3
from todoapp.config import Config
import logging

LOGGER = logging.getLogger(__name__)


class DbConnector:
    __instance = None
    __conn = None
    @staticmethod
    def getInstance():
        if DbConnector.__instance == None:
            DbConnector()
        return DbConnector.__instance

    def __init__(self):
        if DbConnector.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            DbConnector.__instance = self

    def get_connection(self):
        if not self.__conn:
            self.__conn = sqlite3.connect(':memory:',check_same_thread=False)
            self.__conn.row_factory = sqlite3.Row
        return self.__conn

    def run_query(self, query, args):
        connection = self.get_connection()
        cur = connection.cursor()
        result = cur.execute(query, args)
        connection.commit()
        return result

    def init_db(self):
        LOGGER.info('initializing db')
        connection = self.get_connection()
        with open('schema.sql') as f:
            connection.executescript(f.read())
        connection.commit()

    def get_db(self):
        return self.get_connection()

    def get_task(self, task_name):
        connection = self.get_connection()
        task = connection.execute("select * from tasks where task_name = ?", (task_name, )).fetchone()
        return task

    def check_not_completed_and_exists(self, task_name):
        connection = self.get_connection()
        task = connection.execute("select * from tasks where task_name = ? and task_status = ?", (task_name, Config.NEW_TASK)).fetchone()
        return task

    def check_completed_and_exists(self, task_name):
        connection = self.get_connection()
        task = connection.execute("select * from tasks where task_name = ? and task_status = ?", (task_name, Config.COMPLETED_TASK)).fetchone()
        return task

    def get_tasks(self, completed=False):
        connection = self.get_connection()
        query = 'SELECT * FROM tasks where active = true' if not completed else 'SELECT * FROM tasks where active = true and task_status = {}'.format(Config.COMPLETED_TASK)
        tasks_fetch = connection.execute(query).fetchall()
        return tasks_fetch

    def create(self, task_name):
        result = self.run_query("INSERT INTO tasks (task_name) VALUES (?)", (task_name,))
        return result

    def update(self, old_task_name, new_task_name):
        result = self.run_query("update tasks set task_name = ? where task_name = ? and task_status = ?", (new_task_name, old_task_name, Config.NEW_TASK))
        return result

    def set_task_compete(self, task_name):
        result = self.run_query("update tasks set task_status = ? where task_name = ?", (Config.COMPLETED_TASK, task_name))
        return result

    def undo_task(self, task_name):
        result = self.run_query("update tasks set task_status = ? where task_name = ?", (Config.NEW_TASK, task_name))
        return result

    def delete_task(self, task_name):
        result = self.run_query("delete from tasks where task_name = ?", (task_name, ))
        return result
