"""Test cases to unit test server.py."""
import server
import unittest
import tempfile
import os
import json


class TestServer(unittest.TestCase):
    """Mock database by creating a temporary file.
       This function is executed for each test case execution.
    """
    def setUp(self):
        self.db_fd, server.app.config['DATABASE'] = tempfile.mkstemp()
        server.app.testing = True
        self.app = server.app.test_client()
        with server.app.app_context():
            server.init_db()

    """Testing register method of server."""
    def test_register(self):
        emp_data_dict = {"fname": "Aarti", "lname": "Walimbe",
                         "phoneno": "9501879571", "emailid": "aarti@gmail.com",
                         "salary": 25000.00, "bdate": "1995-12-12",
                         "jdate": "2017-06-03"}
        headers = {"Content-Type": "application/json"}
        response = self.app.post('/register', data=json.dumps(emp_data_dict),
                                 headers=headers)
        self.assertEqual(response.status_code, 200)

    """Testing get_all_emp method of server."""
    def test_get_all_emp(self):
        response = self.app.get('/allemployees')
        self.assertEqual(response.status_code, 200)

    """Testing check_emp method of server."""
    def test_check_emp(self):
        emp_dict = {"eid": "1"}
        headers = {"Content-Type": "application/json"}
        response = self.app.get('/checkemp', data=json.dumps(emp_dict),
                                headers=headers)
        self.assertEqual(response.status_code, 200)

    """Testing update method of server."""
    def test_update(self):
        emp_data_dict = {"eid": "1", "fname": "Aarti",
                         "lname": "Walimbe", "phoneno": "9464545201",
                         "emailid": "aarti@xoriant.com",
                         "salary": 25000.00, "bdate": "1995-12-12",
                         "jdate": "2017-06-03"}
        headers = {"Content-Type": "application/json"}
        response = self.app.put('/updateemp', data=json.dumps(emp_data_dict),
                                headers=headers)
        self.assertEqual(response.status_code, 200)

    """Testing delete_emp method of server."""
    def test_delete_emp(self):
        emp_dict = {"eid": "1"}
        headers = {"Content-Type": "application/json"}
        response = self.app.delete('/deleteemp', data=json.dumps(emp_dict),
                                   headers=headers)
        self.assertEqual(response.status_code, 200)

    """Destroy the temporary file created by SetUp method.
       This function is executed for each test case execution.
    """
    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(server.app.config['DATABASE'])


"""Executing test cases."""
if __name__ == '__main__':
    unittest.main()

