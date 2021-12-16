from todoapp.dbconnector import DbConnector
import sqlite3
from todoapp.config import Config
import logging

LOGGER = logging.getLogger(__name__)


class Task:
    task_id = None
    task_name = None
    task_status = Config.NEW_TASK
    active = True

    def __init__(self, task=None):
        if task:
            self.task_id = task[0]
            self.task_name = task[1]
            self.task_status = task[2]
            self.active = task[3]

    @staticmethod
    def create(task_name):
        try:
            DbConnector.getInstance().create(task_name)
        except sqlite3.IntegrityError as e:
            raise Exception('{} already exists'.format(task_name))
        except Exception as e:
            LOGGER.error('create task error', e)
            raise Exception('something went wrong')

    @staticmethod
    def update(old_task_name, new_task_name):
        try:
            DbConnector.getInstance().update(old_task_name, new_task_name)
        except sqlite3.IntegrityError as e:
            raise Exception('{} already exists'.format(new_task_name))
        except Exception as e:
            LOGGER.error('update task error', e)
            raise Exception('something went wrong')

    @staticmethod
    def set_task_compete(task_name):
        try:
            DbConnector.getInstance().set_task_compete(task_name)
        except Exception as e:
            LOGGER.error('set task completed error', e)
            raise Exception('something went wrong')

    @staticmethod
    def undo_task(task_name):
        try:
            DbConnector.getInstance().undo_task(task_name)
        except Exception as e:
            LOGGER.error('undo task error', e)
            raise Exception('something went wrong')

    @staticmethod
    def delete_task(task_name):
        try:
            DbConnector.getInstance().delete_task(task_name)
        except Exception as e:
            LOGGER.error('delete task error', e)
            raise Exception('something went wrong')

    def get_status(self):
        if self.task_status == Config.NEW_TASK:
            return Config.NEW_TASK_STR
        else:
            return Config.COMPLETED_TASK_STR

    def to_json(self):
        return {
            'task_name': self.task_name,
            'task_status': self.get_status(),
            'task_status_raw': self.task_status,
        }

    @staticmethod
    def get_tasks(completed=False):
        try:
            tasks = DbConnector.getInstance().get_tasks(completed)
            tasks_lists = []
            for task in tasks:
                tasks_lists.append(Task(task))
            return tasks_lists
        except Exception as e:
            LOGGER.error('get tasks error', e)
            raise Exception('something went wrong')

    @staticmethod
    def get_task(task_name):
        try:
            return Task(DbConnector.getInstance().get_task(task_name))
        except Exception as e:
            LOGGER.error('get task error', e)
            raise Exception('something went wrong')
