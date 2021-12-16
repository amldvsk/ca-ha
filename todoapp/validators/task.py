from marshmallow import Schema, fields, validates, ValidationError
from marshmallow.validate import Length
from todoapp.dbconnector import DbConnector
import logging
LOGGER = logging.getLogger(__name__)


class CompleteTask(Schema):
    task = fields.Str(required=True, validate=Length(max=250))

    @validates('task')
    def check_not_completed_and_exists(self, data):
        check = DbConnector.getInstance().check_not_completed_and_exists(data)
        if not check:
            raise ValidationError("can't complete task")


class UndoTask(Schema):
    task = fields.Str(required=True, validate=Length(max=250))

    @validates('task')
    def check_completed_and_exists(self, data):
        check = DbConnector.getInstance().check_completed_and_exists(data)
        LOGGER.debug('check_completed_and_exists', check)
        if not check:
            raise ValidationError("can't undo task")


class DeleteTask(Schema):
    task = fields.Str(required=True, validate=Length(max=250))

    @validates('task')
    def check_exists(self, data):
        check = DbConnector.getInstance().get_task(data)
        LOGGER.debug('check_exists', check)
        if check['active'] == 0:
            raise ValidationError("can't delete task")


class CreateTask(Schema):
    task_name = fields.Str(required=True, validate=Length(max=250))
    task_status = fields.Int()


class UpdateTask(Schema):
    task = fields.Str(required=True, validate=Length(max=250))
    task_name = fields.Str(required=True, validate=Length(max=250))

    @validates('task')
    def check_not_completed_and_exists(self, data):
        check = DbConnector.getInstance().check_not_completed_and_exists(data)
        LOGGER.debug('check_not_completed_and_exists', check)
        if not check:
            raise ValidationError("can't update task")