# Student Management System

Welcome to the Student Management System project! This project is a student management system that utilizes PyQt6 for the frontend interface and MySQL for the backend database. The system provides full CRUD (Create, Read, Update, Delete) operations on student records. The project is focused mainly at Object-Oriented Programming (OOP) approach.

## Features

- Create, Read, Update, and Delete student records.
- Frontend user interface built with PyQt6 library.
- Backend database powered by MySQL.
- Object-Oriented Programming (OOP) design principles.

## Installation and Usage

1. Clone the repository:

        git clone <repository_url>



2. Create and activate a virtual environment (optional, but recommended):

        python3 -m venv env
        source env/bin/activate # On macOS/Linux
        .\env\Scripts\activate # On Windows




3. Install the project dependencies:

        pip install -r requirements.txt



4. Set up a MySQL database:

   - Install and configure a MySQL database server.
   - Create a new database for the student management system.

5. Configure the database connection:

   - Open the `main.py` file.
   - Modify the connection properties in the `DatabaseConnection` class to match your MySQL database configuration.
   - The students DDL script is included in the project.

6. Run the application:

        python main.py




7. Interact with the Student Management System through the PyQt6 user interface.

## Project Structure

The project follows an Object-Oriented Programming (OOP) design and has the following structure:

- `main.py`: The main Python script to run the PyQt6 user interface and interact with the student management system, database connection and all the functions that interact with the database.