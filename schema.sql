DROP TABLE IF EXISTS tasks;

CREATE TABLE tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task_name TEXT NOT NULL UNIQUE,
    task_status INTEGER DEFAULT 10,
    active Boolean default True
);


CREATE INDEX task_name_idx
ON tasks(task_name);