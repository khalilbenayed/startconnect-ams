import unittest
from models import Student
from tests.utils import use_test_database


class StudentTest(unittest.TestCase):
    @use_test_database
    def test_create(self):
        test_student_1 = {
            'first_name': 'test',
            'last_name': 'test',
            'email': 'test@test.com',
            'password': 'test'
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


if __name__ == '__main__':
    unittest.main()
