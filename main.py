import sys
from PyQt6.QtWidgets import QApplication, QVBoxLayout, QLabel, QWidget, QGridLayout, \
    QLineEdit, QPushButton, QMainWindow, QTableWidget, QTableWidgetItem, QDialog, QComboBox, QToolBar, QStatusBar, QMessageBox
from PyQt6.QtGui import QAction, QIcon
from datetime import datetime
import mysql.connector


class DatabaseConnection:
    def __init__(self, host="", user="root", password="", database=""):
        self.database = database
        self.host = host
        self.user = user
        self.password = password


    def connect(self):
        connection = mysql.connector.connect(host=self.host, user=self.user, password=self.password,  database=self.database)
        return connection


class MainWindows(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Managment System")
        self.resize(600, 400)

        file_menu_item = self.menuBar().addMenu("&File")
        help_menu_item = self.menuBar().addMenu("&Help")

        add_student_action = QAction(QIcon("icons/add.png"),"Add Student", self)
        add_student_action.triggered.connect(self.insert)
        file_menu_item.addAction(add_student_action)

        search_student_action = QAction(QIcon("icons/search.png"), "Search Student", self)
        search_student_action.triggered.connect(self.search)
        file_menu_item.addAction(search_student_action)

        reset_action = QAction(QIcon("icons/reset.png"), "Reset List", self)
        reset_action.triggered.connect(self.load_data)
        file_menu_item.addAction(reset_action)

        about_action = QAction("About", self)
        help_menu_item.addAction(about_action)
        about_action.setMenuRole(QAction.MenuRole.NoRole)
        about_action.triggered.connect(self.about)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("ID", "Name", "Course", "Mobile"))
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)

        #Create toolbar and add the elements
        toolbar = QToolBar()
        toolbar.setMovable(True)
        self.addToolBar(toolbar)
        toolbar.addAction(add_student_action)
        toolbar.addAction(search_student_action)
        toolbar.addAction(reset_action)

        #Create a status bar and add functionalities
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)

        #Detect a cell click
        self.table.cellClicked.connect(self.cell_clicked)

    def cell_clicked(self):
        edit_button = QPushButton("Edit Record")
        edit_button.clicked.connect(self.edit)

        delete_button = QPushButton("Delete Record")
        delete_button.clicked.connect(self.delete)

        children = self.findChildren(QPushButton)
        if children:
            for child in children:
                self.statusbar.removeWidget(child)

        self.statusbar.addWidget(edit_button)
        self.statusbar.addWidget(delete_button)


    def load_data(self):
        connection = DatabaseConnection().connect()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM students")
        result = cursor.fetchall()
        self.table.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        connection.close()

    def insert(self):
        dialog = InsertDialog()
        dialog.exec()

    def search(self):
        dialog = SearchDialog()
        dialog.exec()

    def load_search_results(self, results):
        self.table.setRowCount(0)
        for row_number, row_data in enumerate(results):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def edit(self):
        dialog = EditDialog()
        dialog.exec()

    def delete(self):
        dialog = DeleteDialog()
        dialog.exec()

    def about(self):
        dialog = AboutDialog()
        dialog.exec()


class AboutDialog(QMessageBox):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("About")
        content = """
        This is an app that was created for managing students that are following a course.
        In this app we can use CRUD operations.
        """
        self.setText(content)

class EditDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Update Student Data")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        #Get selected student from the table
        index = mainWindow.table.currentRow()
        student_name = mainWindow.table.item(index, 1).text()

        #Get id from the selected item
        self.student_id = mainWindow.table.item(index, 0).text()

        # Student name Widget
        self.student_name = QLineEdit(student_name)
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        # Combo courses
        course_name = mainWindow.table.item(index, 2).text()
        self.course_name = QComboBox()
        courses = ["Biology", "Math", "Astronomy", "Physics"]
        self.course_name.addItems(courses)
        self.course_name.setCurrentText(course_name)
        layout.addWidget(self.course_name)

        # Add mobile widget
        mobile = mainWindow.table.item(index, 3).text()
        self.mobile = QLineEdit(mobile)
        # self.mobile.setCurrentText(mobile)
        layout.addWidget(self.mobile)

        button = QPushButton("Update")
        button.clicked.connect(self.update_student)
        layout.addWidget(button)

        self.setLayout(layout)

    def update_student(self):
        connection = DatabaseConnection().connect()
        cursor = connection.cursor()
        cursor.execute("UPDATE students SET name = %s, course = %s, mobile = %s WHERE id = %s",
                       (self.student_name.text(), self.course_name.itemText(self.course_name.currentIndex()), self.mobile.text(), self.student_id))
        connection.commit()
        cursor.close()
        connection.close()
        #Refresh the table
        mainWindow.load_data()


class DeleteDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Delete Student")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        # Get selected student from the table
        index = mainWindow.table.currentRow()
        student_name = mainWindow.table.item(index, 1).text()

        # Get id from the selected item
        self.student_id = mainWindow.table.item(index, 0).text()

        # Student name Widget
        self.student_name = QLineEdit(student_name)
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        # Combo courses
        course_name = mainWindow.table.item(index, 2).text()
        self.course_name = QComboBox()
        courses = ["Biology", "Math", "Astronomy", "Physics"]
        self.course_name.addItems(courses)
        self.course_name.setCurrentText(course_name)
        layout.addWidget(self.course_name)

        # Add mobile widget
        mobile = mainWindow.table.item(index, 3).text()
        self.mobile = QLineEdit(mobile)
        # self.mobile.setCurrentText(mobile)
        layout.addWidget(self.mobile)

        button = QPushButton("Delete")
        button.clicked.connect(self.delete_student)
        button.setStyleSheet("background-color: red; color: white;")
        layout.addWidget(button)

        self.setLayout(layout)

    def delete_student(self):
        connection = DatabaseConnection().connect()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM students WHERE id = %s",
                       (self.student_id,))
        connection.commit()
        cursor.close()
        connection.close()
        # Refresh the table
        mainWindow.load_data()




class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Insert Student Data")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        # Student name Widget
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        # Combo courses
        self.course_name = QComboBox()
        courses = ["Biology", "Math", "Astronomy", "Physics"]
        self.course_name.addItems(courses)
        layout.addWidget(self.course_name)

        # Add mobile widget
        self.mobile = QLineEdit()
        self.mobile.setPlaceholderText("mobile")
        layout.addWidget(self.mobile)

        button = QPushButton("Register")
        button.clicked.connect(self.add_student)
        layout.addWidget(button)

        self.setLayout(layout)

    def add_student(self):
        name = self.student_name.text()
        course = self.course_name.itemText(self.course_name.currentIndex())
        mobile = self.mobile.text()
        connection = DatabaseConnection().connect()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO students (name, course, mobile) VALUES (%s, %s, %s)",
                       (name, course, mobile))
        connection.commit()
        cursor.close()
        connection.close()
        mainWindow.load_data()


class SearchDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Search Student")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        self.student_search = QLineEdit()
        self.student_search.setPlaceholderText("Student name")
        layout.addWidget(self.student_search)

        search_button = QPushButton("Search")
        search_button.clicked.connect(self.search_student)
        layout.addWidget(search_button)

        self.setLayout(layout)

    def search_student(self, layout=None):
        connection = DatabaseConnection().connect()
        cursor = connection.cursor()
        user_input = self.student_search.text()
        cursor.execute("SELECT * FROM students WHERE name LIKE CONCAT('%', %s, '%')", (user_input,))
        result = cursor.fetchall()
        mainWindow.load_search_results(result)
        connection.close()

app = QApplication(sys.argv)
mainWindow = MainWindows()
mainWindow.show()
mainWindow.load_data()
sys.exit(app.exec())
