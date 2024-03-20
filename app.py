from flask import Flask, render_template, request, redirect, jsonify,url_for
import pymysql
from wtforms import Form, StringField, TextAreaField, DateField, BooleanField, validators
from flask_swagger_ui import get_swaggerui_blueprint



app = Flask(__name__)



# MySQL Configuration

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Dheeraj@123ms'
app.config['MYSQL_DB'] = 'todo_db'



db = pymysql.connect(host=app.config['MYSQL_HOST'],
                     user=app.config['MYSQL_USER'],
                     password=app.config['MYSQL_PASSWORD'],
                     db=app.config['MYSQL_DB'],
                     charset='utf8mb4',
                     cursorclass=pymysql.cursors.DictCursor)


cursor = db.cursor()


# TaskForm definition
class TaskForm(Form):
    title = StringField('Title', validators=[validators.DataRequired()])
    description = TextAreaField('Description')
    due_date = DateField('Due Date', format='%Y-%m-%d', validators=[validators.DataRequired()])


class Task:
    def __init__(self, id, title, description, due_date, completed):
        self.id = id
        self.title = title
        self.description = description
        self.due_date = due_date
        self.completed = completed


def create_task(title, description, due_date):
    sql = "INSERT INTO tasks (title, description, due_date) VALUES (%s, %s, %s)"
    cursor.execute(sql, (title, description, due_date))
    db.commit()



def get_tasks():
    sql = "SELECT * FROM tasks"
    cursor.execute(sql)
    tasks = []
    for row in cursor.fetchall():
        task = Task(row['id'], row['title'], row['description'], row['due_date'], row['completed'])
        tasks.append(task)
    return tasks

def get_task_by_id_from_database(task_id):
    sql = "SELECT * FROM tasks WHERE id = %s"
    cursor.execute(sql, (task_id,))
    row = cursor.fetchone()

    if row:
        task = Task(row['id'], row['title'], row['description'], row['due_date'], row['completed'])
        return task
    else:
        return None


def update_task(task_id, title, description, due_date, completed):
    sql = "UPDATE tasks SET title=%s, description=%s, due_date=%s, completed=%s WHERE id=%s"
    cursor.execute(sql, (title, description, due_date, completed, task_id))
    db.commit()



# Routes
    
#GET
@app.route('/', methods=['GET'])
def index():
    tasks = get_tasks()
    return render_template('index.html', tasks=tasks)


#POST
@app.route('/add_task', methods=['GET', 'POST'])
def add_task():
    if request.method == 'POST':
        print("Received a POST request to add a task")
        form = TaskForm(request.form)
        if form.validate():
            title = form.title.data
            description = form.description.data
            due_date = form.due_date.data
            create_task(title, description, due_date)
            print(form)
            return redirect(url_for('index'))
        else:
            return render_template('add_task.html', form=form)
    else:
        print("Rendering add task form for GET request")
        # If it's a GET request, render the add task form
        form = TaskForm()
        return render_template('add_task.html', form=form)



#PUT
@app.route('/update_task/<int:task_id>', methods=['PUT'])
def update_task_route(task_id):
    form = TaskForm(request.form)
    if form.validate():
        title = form.title.data
        description = form.description.data
        due_date = form.due_date.data
        completed = 'completed' in request.form
        update_task(task_id, title, description, due_date, completed)
        return jsonify({"message": "Task updated successfully"})
    else:
        return jsonify({"error": "Validation failed"}), 400


#DELETE 
@app.route('/delete_task/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    if request.method == 'DELETE':
        print("Received a DELETE request to delete task with ID:", task_id)
        try:
            # Perform deletion logic here
            sql = "DELETE FROM tasks WHERE id = %s"
            cursor.execute(sql, (task_id,))
            db.commit()
            return jsonify({"message": "Task deleted successfully"})
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        # If the request method is not DELETE, return a Method Not Allowed error
        return jsonify({"error": "Method Not Allowed"}), 405



# Swagger
SWAGGER_URL = '/swagger'
API_URL = '/swagger.json'


swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Todo Application"
    }
)


app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

@app.route('/swagger.json')
def swagger_spec():
    spec = {
        "swagger": "2.0",
        "info": {
            "title": "Todo Application API",
            "description": "API for managing tasks in a todo application",
            "version": "1.0"
        },
        "paths": {
            "/add_task": {
                "post": {
                    "summary": "Add a new task",
                    "parameters": [
                        {
                            "name": "title",
                            "in": "formData",
                            "description": "Title of the task",
                            "required": True,
                            "type": "string"
                        },
                        {
                            "name": "description",
                            "in": "formData",
                            "description": "Description of the task",
                            "required": False,
                            "type": "string"
                        },
                        {
                            "name": "due_date",
                            "in": "formData",
                            "description": "Due date of the task (format: YYYY-MM-DD)",
                            "required": True,
                            "type": "string",
                            "format": "date"
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Task added successfully"
                        },
                        "400": {
                            "description": "Validation failed"
                        }
                    }
                }
            },
            "/update_task/{task_id}": {
                "put": {
                    "summary": "Update an existing task",
                    "parameters": [
                        {
                            "name": "task_id",
                            "in": "path",
                            "description": "ID of the task to update",
                            "required": True,
                            "type": "integer"
                        },
                        {
                            "name": "title",
                            "in": "formData",
                            "description": "New title of the task",
                            "required": True,
                            "type": "string"
                        },
                        {
                            "name": "description",
                            "in": "formData",
                            "description": "New description of the task",
                            "required": False,
                            "type": "string"
                        },
                        {
                            "name": "due_date",
                            "in": "formData",
                            "description": "New due date of the task (format: YYYY-MM-DD)",
                            "required": True,
                            "type": "string",
                            "format": "date"
                        },
                        {
                            "name": "completed",
                            "in": "formData",
                            "description": "Whether the task is completed",
                            "required": False,
                            "type": "boolean"
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Task updated successfully"
                        },
                        "400": {
                            "description": "Validation failed"
                        }
                    }
                }
            },
            "/delete_task/{task_id}": {
                "delete": {
                    "summary": "Delete a task",
                    "parameters": [
                        {
                            "name": "task_id",
                            "in": "path",
                            "description": "ID of the task to delete",
                            "required": True,
                            "type": "integer"
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Task deleted successfully"
                        },
                        "404": {
                            "description": "Task not found"
                        }
                    }
                }
            },
            "/": {
                "get": {
                    "summary": "Get all tasks",
                    "responses": {
                        "200": {
                            "description": "Tasks retrieved successfully"
                        }
                    }
                }
            }
        }
    }

    return jsonify(spec)



if __name__ == '__main__':

    app.run(debug=True)

