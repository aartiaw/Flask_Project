"""Client app to consume REST APIs."""
import requests
import json


def register():
    """Option to register an employee. Get all details of
       employee to be registered.
    """
    fname = raw_input("Enter firstname: ")
    lname = raw_input("Enter lastname: ")
    phoneno = raw_input("Enter phone number: ")
    emailid = raw_input("Enter email id: ")
    salary = float(raw_input("Enter salary in rupees:  "))
    birth_date = raw_input("Enter birth date (YYYY-MM-DD):  ")
    joining_date = raw_input("Enter joining date (YYYY-MM-DD):  ")

    emp_data_dict = {"fname": fname, "lname": lname,
                     "phoneno": phoneno, "emailid": emailid,
                     "salary": salary, "bdate": birth_date,
                     "jdate": joining_date}

    headers = {"Content-Type": "application/json"}
    register_request = requests.post("http://127.0.0.1:5000/register",
                                     data=json.dumps(emp_data_dict),
                                     headers=headers)
    return register_request


def display():
    """Option to get all employees' detail."""
    show_request = requests.get("http://127.0.0.1:5000/allemployees")
    return show_request


def check_employee():
    """Check if particular employee exists or not by knowing
       employee id.
    """
    emp_id = raw_input("Enter employee id: ")
    emp_dict = {"eid": emp_id}

    headers = {"Content-Type": "application/json"}
    """Check if employee with given id exists or not."""
    checkemp_request = requests.get("http://127.0.0.1:5000/checkemp",
                                    data=json.dumps(emp_dict),
                                    headers=headers)
    return checkemp_request


def update(emp_id):
    """Option to update details of given employee id."""
    print "--------New details for Employee--------"
    fname = raw_input("Enter firstname: ")
    lname = raw_input("Enter lastname: ")
    phoneno = raw_input("Enter phone number: ")
    emailid = raw_input("Enter email id: ")
    salary = float(raw_input("Enter salary in rupees:  "))
    birth_date = raw_input("Enter birth date (YYYY-MM-DD):  ")
    joining_date = raw_input("Enter joining date (YYYY-MM-DD):  ")

    emp_data_dict = {"eid": emp_id, "fname": fname, "lname": lname,
                     "phoneno": phoneno, "emailid": emailid,
                     "salary": salary, "bdate": birth_date,
                     "jdate": joining_date}

    headers = {"Content-Type": "application/json"}
    update_request = requests.put("http://127.0.0.1:5000/updateemp",
                                  data=json.dumps(emp_data_dict),
                                  headers=headers)
    return update_request


def delete():
    """Option to delete an employee from database by
       knowing his employee id.
    """
    emp_id = raw_input("Enter employee id to delete: ")
    emp_dict = {"eid": emp_id}
    headers = {"Content-Type": "application/json"}
    delete_request = requests.delete("http://127.0.0.1:5000/deleteemp",
                                     data=json.dumps(emp_dict),
                                     headers=headers)
    return delete_request


"""Execute the application."""
if __name__ == "__main__":
    while True:
        """Display choices of operations to user and select one option."""
        print "1.Register employee\n2.Get all employee details\n" \
              "3.Update employee\n4.Delete employee"

        option = int(raw_input("Enter your choice: "))

        if option == 1:
            """Call register method if user enter option = 1."""
            register_request = register()
            response_dict = register_request.json()
            print response_dict["response"]

        elif option == 2:
            """Call display method if user enter option = 2."""
            show_request = display()
            response_dict = show_request.text
            print response_dict

        elif option == 3:
            """Call check_employee method if user enter option = 3."""
            checkemp_request = check_employee()
            response_value = checkemp_request.json()

            """If employee exists, call update method for that employee,
               else give appropriate message.
            """
            if response_value["response"] != "":
                update_request = update(response_value["response"])
                response_dict = update_request.json()
                print "Record updated successfully!"
            else:
                print "This employee id doesn't exists!"

        elif option == 4:
            """Call delete method if user enter option = 4."""
            delete_request = delete()
            response_value = delete_request.json()
            print response_value["response"]

        else:
            """Break the while loop for any other option entered
               by the user.
            """
            break

