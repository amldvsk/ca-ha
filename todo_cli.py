import click
import requests

class TodoApi:
    url = 'http://localhost:5000'

    @staticmethod
    def list_tasks(completed=None):
        res = requests.get(TodoApi.url if not completed else TodoApi.url+"?completed=1")
        return res.json()

    @staticmethod
    def create_task(task_name):
        res = requests.post(TodoApi.url, data={'task_name': task_name})
        return res.json()

    @staticmethod
    def update_task(task_name, new_task_name):
        res = requests.post(TodoApi.url+"/"+task_name, data={'task_name': new_task_name})
        return res.json()

    @staticmethod
    def complete_task(task_name):
        res = requests.get(TodoApi.url + "/complete/" + task_name)
        return res.json()

    @staticmethod
    def undo_task(task_name):
        res = requests.get(TodoApi.url + "/undo/" + task_name)
        return res.json()

    @staticmethod
    def delete_task(task_name):
        res = requests.get(TodoApi.url + "/delete/" + task_name)
        return res.json()

@click.command()
@click.argument('command', nargs=1)
@click.argument('args', nargs=-1)
def main(command, args):
    if command == 'list-tasks' or command == 'list-completed-tasks':
        tasks = TodoApi.list_tasks(True if command == 'list-completed-tasks' else False)
        if tasks['success']:
            click.echo('%-20s%-20s' % ('Name', 'Completed'))
            for task in tasks['tasks']:
                click.echo('%-20s%-20s' % (task['task_name'], '+' if task['task_status_raw'] == 20 else '-'))
        else:
            click.echo(tasks['msg'])
    if command == 'add-task':
        create = TodoApi.create_task(args[0])
        if create['success']:
            click.echo('{} created successfully'.format(args[0]))
        else:
            click.echo(create['msg'])
    if command == 'update-task':
        create = TodoApi.update_task(args[0], args[1])
        if create['success']:
            click.echo('{} update successfully to {}'.format(args[0], args[1]))
        else:
            click.echo(create['msg'])
    if command == 'complete-task':
        create = TodoApi.complete_task(args[0])
        if create['success']:
            click.echo('{} complete successfully'.format(args[0]))
        else:
            click.echo(create['msg'])
    if command == 'undo-task':
        create = TodoApi.undo_task(args[0])
        if create['success']:
            click.echo('{} undo successfully'.format(args[0]))
        else:
            click.echo(create['msg'])
    if command == 'delete-task':
        create = TodoApi.delete_task(args[0])
        if create['success']:
            click.echo('{} deleted successfully'.format(args[0]))
        else:
            click.echo(create['msg'])


if __name__ == '__main__':
    main()