from setuptools import setup
setup(
    name="todoapp",
    version="1.0.1",
    install_requires=[
        'attrs',
        'certifi',
        'charset-normalizer',
        'click',
        'idna',
        'iniconfig',
        'itsdangerous',
        'Jinja2',
        'MarkupSafe',
        'packaging',
        'pluggy',
        'py',
        'pyparsing',
        'pytest',
        'requests',
        'toml',
        'urllib3',
        'Werkzeug'
    ],
    entry_points={
        "console_scripts": [
            "todo = todo_cli:main",
        ],
    },
)