"""Server app to create REST APIs."""
import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, jsonify

app = Flask(__name__)
app.config.from_object(__name__)

"""Load default config and override config from an environment variable."""
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, "users.db"),
    SECRET_KEY="development key",
))
app.config.from_envvar("FLASKR_SETTINGS", silent=True)

app.url_map.strict_slashes = False


def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config["DATABASE"])
    rv.row_factory = sqlite3.Row
    return rv


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, "sqlite_db"):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


def init_db():
    db = get_db()
    with app.open_resource("schema.sql", mode="r") as f:
        db.cursor().executescript(f.read())
    db.commit()


@app.cli.command("initdb")
def initdb_command():
    """Initializes the database."""
    init_db()
    print "Initialized the database."


@app.route("/register", methods=["POST"])
def register():
    """REST API to insert new employee details into database."""
    emp_data = request.get_json()
    db = get_db()
    db.execute("insert into employee" +
               "(fname, lname, phoneno, emailid, sal, bdate, jdate)" +
               "values (?, ?, ?, ?, ?, ?, ?)", [emp_data["fname"],
                                                emp_data["lname"],
                                                emp_data["phoneno"],
                                                emp_data["emailid"],
                                                emp_data["salary"],
                                                emp_data["bdate"],
                                                emp_data["jdate"]])
    db.commit()
    response = jsonify({"response": "Registration successful!"})
    return response


@app.route("/allemployees", methods=["GET"])
def get_all_emp():
    """REST API to get details of all employees."""
    db = get_db()
    cur = db.execute("select * from employee")
    entries = [dict(emp_id=row[0], fname=row[1], lname=row[2], phoneno=row[3],
                    emailid=row[4], sal=row[5], bdate=row[6], jdate=row[7])
               for row in cur.fetchall()]
    return jsonify(entries)


@app.route("/checkemp", methods=["GET"])
def check_emp():
    """REST API to check if employee with given id exists in database
       or not.
    """
    emp_dict = request.get_json()
    db = get_db()
    cur = db.execute("select * from employee where id=?",
                     (emp_dict["eid"]))

    if cur.fetchone():
        return jsonify({"response": emp_dict["eid"]})
    else:
        return jsonify({"response": ""})


@app.route("/updateemp", methods=["PUT"])
def update_emp():
    """REST API to update details of given employee."""
    emp_data = request.get_json()
    db = get_db()
    cur = db.execute("update employee set fname=?, lname=?, phoneno=?," +
                     "emailid=?, sal=?, bdate=?, jdate=? where id=?",
                     (emp_data["fname"], emp_data["lname"],
                      emp_data["phoneno"], emp_data["emailid"],
                      emp_data["salary"], emp_data["bdate"],
                      emp_data["jdate"], emp_data["eid"]))
    db.commit()
    response = jsonify({"response": "Record updated successfully!"})
    return response


@app.route("/deleteemp", methods=["DELETE"])
def delete_emp():
    """REST API to delete an employee with given id."""
    emp_dict = request.get_json()
    db = get_db()

    """Check if employee with given id exists into database. If exists,
       then delete, else give appropriate message.
    """
    cur = db.execute("select * from employee where id=?",
                     (emp_dict["eid"]))

    if cur.fetchone():
        cur = db.execute("delete from employee where id=?",
                         (emp_dict["eid"]))
        db.commit()
        response = jsonify({"response": "Record deleted successfully!"})

    else:
        response = jsonify({"response": "This employee id doesn't exists!"})

    return response


"""Execute the application."""
if __name__ == "__main__":
    app.run()

