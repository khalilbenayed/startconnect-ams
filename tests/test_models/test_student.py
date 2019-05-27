import unittest
from models import Student
from tests.utils import use_test_database


class StudentTest(unittest.TestCase):
    @use_test_database
    def test_create_1(self):
        test_student_1 = {
            'first_name': 'test',
            'last_name': 'test',
            'email': 'test@test.com',
            'password': 'test',
            'state': 'TEST',
        }
        return_result = Student.create(**test_student_1)
        self.assertEqual(test_student_1.get('first_name'), return_result.first_name)
        self.assertEqual(test_student_1.get('last_name'), return_result.last_name)
        self.assertEqual(test_student_1.get('email'), return_result.email)
        self.assertEqual(test_student_1.get('password'), return_result.password)

        get_result = Student.get(id=return_result.id)
        self.assertEqual(test_student_1.get('first_name'), get_result.first_name)
        self.assertEqual(test_student_1.get('last_name'), get_result.last_name)
        self.assertEqual(test_student_1.get('email'), get_result.email)
        self.assertEqual(test_student_1.get('password'), get_result.password)

    @use_test_database
    def test_create_2(self):
        test_student_1 = {
            'first_name': 'test_1',
            'last_name': 'test_1',
            'email': 'test_1@test.com',
            'password': 'test',
            'state': 'TEST',
        }
        test_student_2 = {
            'first_name': 'test_2',
            'last_name': 'test_2',
            'email': 'test_2@test.com',
            'password': 'test',
            'state': 'TEST',
        }
        return_result_1 = Student.create(**test_student_1)
        self.assertEqual(test_student_1.get('first_name'), return_result_1.first_name)
        self.assertEqual(test_student_1.get('last_name'), return_result_1.last_name)
        self.assertEqual(test_student_1.get('email'), return_result_1.email)
        self.assertEqual(test_student_1.get('password'), return_result_1.password)
        return_result_2 = Student.create(**test_student_2)
        self.assertEqual(test_student_2.get('first_name'), return_result_2.first_name)
        self.assertEqual(test_student_2.get('last_name'), return_result_2.last_name)
        self.assertEqual(test_student_2.get('email'), return_result_2.email)
        self.assertEqual(test_student_2.get('password'), return_result_2.password)

        get_result_1 = Student.get(id=return_result_1.id)
        self.assertEqual(test_student_1.get('first_name'), get_result_1.first_name)
        self.assertEqual(test_student_1.get('last_name'), get_result_1.last_name)
        self.assertEqual(test_student_1.get('email'), get_result_1.email)
        self.assertEqual(test_student_1.get('password'), get_result_1.password)

        get_result_2 = Student.get(id=return_result_2.id)
        self.assertEqual(test_student_2.get('first_name'), get_result_2.first_name)
        self.assertEqual(test_student_2.get('last_name'), get_result_2.last_name)
        self.assertEqual(test_student_2.get('email'), get_result_2.email)
        self.assertEqual(test_student_2.get('password'), get_result_2.password)


if __name__ == '__main__':
    unittest.main()
