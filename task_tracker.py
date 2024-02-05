from flask import Flask, render_template, request, redirect, url_for
import datetime
import json

app = Flask(__name__)

tasks = []

@app.route('/')
def index():
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    title = request.form['title']
    description = request.form['description']
    due_date = datetime.datetime.strptime(request.form['due_date'], '%Y-%m-%d').date()
    priority = request.form['priority']
    
    task = {
        'title': title,
        'description': description,
        'due_date': due_date,
        'priority': priority,
        'completed': False
    }
    
    tasks.append(task)
    
    return redirect(url_for('index'))

@app.route('/complete/<int:task_id>')
def complete_task(task_id):
    if task_id >= 0 and task_id < len(tasks):
        tasks[task_id]['completed'] = True
    
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    if task_id >= 0 and task_id < len(tasks):
        del tasks[task_id]
    
    return redirect(url_for('index'))

@app.route('/search', methods=['POST'])
def search_tasks():
    keyword = request.form['keyword']
    filtered_tasks = []
    
    for task in tasks:
        if keyword.lower() in task['title'].lower() or keyword.lower() in task['description'].lower():
            filtered_tasks.append(task)
    
    return render_template('index.html', tasks=filtered_tasks)

@app.route('/sort', methods=['POST'])
def sort_tasks():
    sorted_tasks = sorted(tasks, key=lambda task: task['priority'], reverse=True)
    
    return render_template('index.html', tasks=sorted_tasks)

if __name__ == '__main__':
    app.run(debug=True)