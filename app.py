from flask import Flask, render_template_string, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# SQLite database file
DATABASE = 'tasks.db'

def create_table():
    with sqlite3.connect(DATABASE) as connection:
        cursor = connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                completed BOOLEAN
            );
        ''')
        connection.commit()

html_code = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Task Manager</title>
</head>
<body>
    <h1>Task Manager</h1>
    <ul>
        {% for task in tasks %}
            <li>
                {{ task[1] }} - {{ task[2] }} - {{ "Completed" if task[3] else "Not Completed" }}
                <a href="{{ url_for('update', task_id=task[0]) }}">Toggle Status</a>
                <a href="{{ url_for('delete', task_id=task[0]) }}">Delete</a>
            </li>
        {% endfor %}
    </ul>
    <form method="post" action="{{ url_for('add') }}">
        <label for="title">Title:</label>
        <input type="text" name="title" required>
        <label for="description">Description:</label>
        <input type="text" name="description">
        <button type="submit">Add Task</button>
    </form>
</body>
</html>
'''

@app.route('/')
def index():
    create_table()
    with sqlite3.connect(DATABASE) as connection:
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM tasks;')
        tasks = cursor.fetchall()
    return render_template_string(html_code, tasks=tasks)

@app.route('/add', methods=['POST'])
def add():
    title = request.form['title']
    description = request.form['description']
    with sqlite3.connect(DATABASE) as connection:
        cursor = connection.cursor()
        cursor.execute('INSERT INTO tasks (title, description, completed) VALUES (?, ?, ?);', (title, description, False))
        connection.commit()
    return redirect(url_for('index'))

@app.route('/update/<int:task_id>')
def update(task_id):
    with sqlite3.connect(DATABASE) as connection:
        cursor = connection.cursor()
        cursor.execute('UPDATE tasks SET completed = NOT completed WHERE id = ?;', (task_id,))
        connection.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>')
def delete(task_id):
    with sqlite3.connect(DATABASE) as connection:
        cursor = connection.cursor()
        cursor.execute('DELETE FROM tasks WHERE id = ?;', (task_id,))
        connection.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
