from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

# Configure MySQL connection
app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = "pranab@01345"
app.config['MYSQL_DB'] = "todo"

db = MySQL(app)

# Model to interact with the database
class Employee:
    def __init__(self, name, age, contact_no, salary):
        self.name = name
        self.age = age
        self.contact_no = contact_no
        self.salary = salary

    def save(self):
        cur = db.connection.cursor()
        cur.execute("INSERT INTO employees(name, age, contact_no, salary) VALUES (%s, %s, %s, %s)",
                    (self.name, self.age, self.contact_no, self.salary))
        db.connection.commit()
        cur.close()

    @staticmethod
    def get_all():
        cur = db.connection.cursor()
        cur.execute("SELECT * FROM employees")
        employees = cur.fetchall()
        cur.close()
        return employees

    @staticmethod
    def update(id, name, age, contact_no, salary):
        cur = db.connection.cursor()
        cur.execute("UPDATE employees SET name=%s, age=%s, contact_no=%s, salary=%s WHERE id=%s",
                    (name, age, contact_no, salary, id))
        db.connection.commit()
        cur.close()

    @staticmethod
    def delete(id):
        cur = db.connection.cursor()
        cur.execute("DELETE FROM employees WHERE id=%s", [id])
        db.connection.commit()
        cur.close()

# Route to display the form and all employees
@app.route('/')
def index():
    employees = Employee.get_all()
    return render_template('base.html', employees=employees)

# Route to handle adding an employee
@app.route('/add', methods=['POST'])
def add_employee():
    name = request.form['name']
    age = request.form['age']
    contact_no = request.form['contact_no']
    salary = request.form['salary']
    
    employee = Employee(name, age, contact_no, salary)
    employee.save()
    
    return redirect(url_for('index'))

# Route to handle deleting an employee
@app.route('/delete/<int:id>')
def delete_employee(id):
    Employee.delete(id)
    return redirect(url_for('index'))

# Route to handle updating an employee
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_employee(id):
    cur = db.connection.cursor()
    cur.execute("SELECT * FROM employees WHERE id = %s", [id])
    employee = cur.fetchone()
    
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        contact_no = request.form['contact_no']
        salary = request.form['salary']
        
        Employee.update(id, name, age, contact_no, salary)
        return redirect(url_for('index'))

    return render_template('edit.html', employee=employee)

if __name__ == "__main__":
    app.run(debug=True)
