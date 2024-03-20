# To-Do-Application

Description:
This is a simple todo application built with Flask. It allows users to manage their tasks by adding, updating, and deleting them.

Features:
Add tasks with a title, description, and due date.
View all tasks on the main page.
Update task details.
Delete tasks.

Installation:
Clone the repository to your local machine:
bash
Copy code
git clone https://github.com/your_username/todo-application.git
Navigate to the project directory:
bash
Copy code
cd todo-application

Install the required dependencies:
Copy code
pip install -r requirements.txt
Usage
Start the Flask server:
Copy code
python app.py

Open your web browser and navigate to http://localhost:5000 to access the application.
You can add tasks by clicking on the "Add Task" button and filling out the form.
To update or delete tasks, click on the "Update" or "Delete" buttons next to each task on the main page.
API Documentation
You can view the API documentation by navigating to /swagger endpoint in your browser after starting the server.

Project Structure:
app.py: Contains the Flask application code.
templates/: Directory containing HTML templates for the application.

Dependencies:
Flask: Web framework for building the application.
Flask-Swagger-UI: Integration for displaying Swagger UI for API documentation.
PyMySQL: Python MySQL client library.
