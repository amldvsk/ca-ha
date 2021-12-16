from todoapp.dbconnector import DbConnector
from flask import Flask, jsonify, make_response, request
from todoapp.modules.task import Task
from todoapp.validators.task import UndoTask, DeleteTask, UpdateTask, CompleteTask, CreateTask
DbConnector.getInstance().init_db()


def create_app(test_config=None):
    app = Flask(__name__)

    def json_response(status, data):
        response = make_response(
            jsonify(data),
            status,
        )
        response.headers["Content-Type"] = "application/json"
        return response

    @app.route('/', methods=['GET'])
    def get_tasks():
        completed = request.args.get('completed')
        tasks = [task.to_json() for task in Task.get_tasks(completed)]
        return json_response(200, {'success': True, 'tasks': tasks})

    @app.route('/', methods=['POST'])
    def create_task():
        try:
            errors = CreateTask().validate(request.form)
            if errors:
                return json_response(500, {'success': False, 'msg': str(errors)})
            Task.create(request.form['task_name'])
            return json_response(200, {'success': True})
        except Exception as e:
            return json_response(500, {'success': False, 'msg': str(e)})

    @app.route('/<task>', methods=['POST'])
    def update_task(task):
        errors = UpdateTask().validate({**request.form, 'task': task})
        if errors:
            return json_response(500, {'success': False, 'msg': str(errors)})
        Task.update(task, request.form['task_name'])
        return json_response(200, {'success': True})

    @app.route('/complete/<task>', methods=['GET'])
    def complete_task(task):
        errors = CompleteTask().validate({'task': task})
        if errors:
            return json_response(500, {'success': False, 'msg': str(errors)})
        Task.set_task_compete(task)
        return json_response(200, {'success': True})

    @app.route('/undo/<task>', methods=['GET'])
    def undo_task(task):
        errors = UndoTask().validate({'task': task})
        if errors:
            return json_response(500, {'success': False, 'msg': str(errors)})
        Task.undo_task(task)
        return json_response(200, {'success': True})

    @app.route('/delete/<task>', methods=['GET'])
    def delete_task(task):
        errors = DeleteTask().validate({'task': task})
        if errors:
            return json_response(500, {'success': False, 'msg': str(errors)})
        Task.delete_task(task)
        return json_response(200, {'success': True})

    return app