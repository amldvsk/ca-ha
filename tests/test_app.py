import json
from todoapp.modules.task import Task
from todoapp.config import Config
from todoapp.dbconnector import DbConnector


def test_get_all_tasks(client):
    rv = client.get('/')
    data = json.loads(rv.data)
    assert data['success'] == True
    assert len(data['tasks']) == 3


def test_get_only_completed_tasks(client):
    rv = client.get('/?completed=true')
    data = json.loads(rv.data)
    assert data['success'] == True
    assert len(data['tasks']) == 1


def test_create_task(client):
    rv = client.post('/', data={'task_name':'test name'})
    data = json.loads(rv.data)
    assert data['success'] == True
    find = Task.get_task('test name')
    assert find.to_json()['task_name'] == 'test name'


def test_create_task_validation(client):
    rv = client.post('/', data={'name':'test name'})
    data = json.loads(rv.data)
    assert data['success'] == False



def test_create_duplicate_task(client):
    rv = client.post('/', data={'task_name':'test name'})
    data = json.loads(rv.data)
    assert data['success'] == True
    find = Task.get_task('test name')
    assert find.to_json()['task_name'] == 'test name'
    assert client.post('/', data={'task_name':'test name'}).status_code == 500


def test_update_task(client):
    rv = client.post('/', data={'task_name':'test name'})
    data = json.loads(rv.data)
    assert data['success'] == True
    find = Task.get_task('test name')
    assert find.to_json()['task_name'] == 'test name'
    client.post('/test name', data={'task_name': 'test name update'})
    find = Task.get_task('test name update')
    assert find.to_json()['task_name'] == 'test name update'


def test_complete_task(client):
    rv = client.post('/', data={'task_name':'test name'})
    data = json.loads(rv.data)
    assert data['success'] == True
    client.get('/complete/test name')
    find = Task.get_task('test name')
    assert find.to_json()['task_status'] == Config.COMPLETED_TASK_STR


def test_undo_task(client):
    rv = client.post('/', data={'task_name':'test name'})
    data = json.loads(rv.data)
    assert data['success'] == True
    client.get('/complete/test name')
    find = Task.get_task('test name')
    assert find.to_json()['task_status'] == Config.COMPLETED_TASK_STR
    client.get('/undo/test name')
    find = Task.get_task('test name')
    assert find.to_json()['task_status'] == Config.NEW_TASK_STR


def test_delete_task(client):
    rv = client.post('/', data={'task_name': 'test name'})
    data = json.loads(rv.data)
    assert data['success'] == True
    client.get('/delete/test name')    
    find = DbConnector.getInstance().get_db().execute("select * from tasks where task_name = 'test name' and active = true").fetchone()
    assert find == None