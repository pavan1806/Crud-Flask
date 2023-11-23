# app.py
from flask import Flask, render_template, request, redirect, url_for
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

@app.route('/')
def index():
    create_table()
    with sqlite3.connect(DATABASE) as connection:
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM tasks;')
        tasks = cursor.fetchall()
    return render_template('index.html', tasks=tasks)

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
