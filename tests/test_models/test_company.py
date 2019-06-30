import unittest
from models import Company
from tests.utils import use_test_database


class CompanyTest(unittest.TestCase):
    @use_test_database
    def test_create_1(self):
        test_company_1 = {
            'company_name': 'test',
            'email': 'test@test.com',
            'password': 'test',
            'state': 'TEST',
            'address_1': 'test',
            'city': 'toronto',
            'province': 'ON',
            'zipcode': 'xxxxxx',
            'country': 'canada',
            'phone': '123456789'

        }
        return_result = Company.create(**test_company_1)
        self.assertEqual(test_company_1.get('company_name'), return_result.company_name)
        self.assertEqual(test_company_1.get('email'), return_result.email)
        self.assertEqual(test_company_1.get('password'), return_result.password)
        self.assertEqual(test_company_1.get('state'), return_result.state)
        self.assertEqual(test_company_1.get('address_1'), return_result.address_1)
        self.assertEqual(test_company_1.get('address_2'), return_result.address_2)
        self.assertEqual(test_company_1.get('city'), return_result.city)
        self.assertEqual(test_company_1.get('province'), return_result.province)
        self.assertEqual(test_company_1.get('zipcode'), return_result.zipcode)
        self.assertEqual(test_company_1.get('country'), return_result.country)
        self.assertEqual(test_company_1.get('phone'), return_result.phone)

        get_result = Company.get(id=return_result.id)
        self.assertEqual(test_company_1.get('company_name'), get_result.company_name)
        self.assertEqual(test_company_1.get('email'), get_result.email)
        self.assertEqual(test_company_1.get('password'), get_result.password)
        self.assertEqual(test_company_1.get('state'), get_result.state)
        self.assertEqual(test_company_1.get('address_1'), get_result.address_1)
        self.assertEqual(test_company_1.get('address_2'), get_result.address_2)
        self.assertEqual(test_company_1.get('city'), get_result.city)
        self.assertEqual(test_company_1.get('province'), get_result.province)
        self.assertEqual(test_company_1.get('zipcode'), get_result.zipcode)
        self.assertEqual(test_company_1.get('country'), get_result.country)
        self.assertEqual(test_company_1.get('phone'), get_result.phone)

    @use_test_database
    def test_create_2(self):
        test_company_1 = {
            'company_name': 'test_1',
            'email': 'test_1@test.com',
            'password': 'test',
            'state': 'TEST',
            'address_1': 'test_1',
            'city': 'toronto',
            'province': 'ON',
            'zipcode': 'xxxxxx',
            'country': 'canada',
            'phone': '123456789'

        }
        test_company_2 = {
            'company_name': 'test_2',
            'email': 'test_2@test.com',
            'password': 'test',
            'state': 'TEST',
            'address_1': 'test_2',
            'city': 'waterloo',
            'province': 'ON',
            'zipcode': 'xxxxxx',
            'country': 'canada',
            'phone': '987654321'

        }
        return_result_1 = Company.create(**test_company_1)
        self.assertEqual(test_company_1.get('company_name'), return_result_1.company_name)
        self.assertEqual(test_company_1.get('email'), return_result_1.email)
        self.assertEqual(test_company_1.get('password'), return_result_1.password)
        self.assertEqual(test_company_1.get('state'), return_result_1.state)
        self.assertEqual(test_company_1.get('address_1'), return_result_1.address_1)
        self.assertEqual(test_company_1.get('address_2'), return_result_1.address_2)
        self.assertEqual(test_company_1.get('city'), return_result_1.city)
        self.assertEqual(test_company_1.get('province'), return_result_1.province)
        self.assertEqual(test_company_1.get('zipcode'), return_result_1.zipcode)
        self.assertEqual(test_company_1.get('country'), return_result_1.country)
        self.assertEqual(test_company_1.get('phone'), return_result_1.phone)
        return_result_2 = Company.create(**test_company_2)
        self.assertEqual(test_company_2.get('company_name'), return_result_2.company_name)
        self.assertEqual(test_company_2.get('email'), return_result_2.email)
        self.assertEqual(test_company_2.get('password'), return_result_2.password)
        self.assertEqual(test_company_2.get('state'), return_result_2.state)
        self.assertEqual(test_company_2.get('address_1'), return_result_2.address_1)
        self.assertEqual(test_company_2.get('address_2'), return_result_2.address_2)
        self.assertEqual(test_company_2.get('city'), return_result_2.city)
        self.assertEqual(test_company_2.get('province'), return_result_2.province)
        self.assertEqual(test_company_2.get('zipcode'), return_result_2.zipcode)
        self.assertEqual(test_company_2.get('country'), return_result_2.country)
        self.assertEqual(test_company_2.get('phone'), return_result_2.phone)

        get_result_1 = Company.get(id=return_result_1.id)
        self.assertEqual(test_company_1.get('company_name'), get_result_1.company_name)
        self.assertEqual(test_company_1.get('email'), get_result_1.email)
        self.assertEqual(test_company_1.get('password'), get_result_1.password)
        self.assertEqual(test_company_1.get('state'), get_result_1.state)
        self.assertEqual(test_company_1.get('address_1'), get_result_1.address_1)
        self.assertEqual(test_company_1.get('address_2'), get_result_1.address_2)
        self.assertEqual(test_company_1.get('city'), get_result_1.city)
        self.assertEqual(test_company_1.get('province'), get_result_1.province)
        self.assertEqual(test_company_1.get('zipcode'), get_result_1.zipcode)
        self.assertEqual(test_company_1.get('country'), get_result_1.country)
        self.assertEqual(test_company_1.get('phone'), get_result_1.phone)

        get_result_2 = Company.get(id=return_result_2.id)
        self.assertEqual(test_company_2.get('email'), get_result_2.email)
        self.assertEqual(test_company_2.get('password'), get_result_2.password)
        self.assertEqual(test_company_2.get('state'), get_result_2.state)
        self.assertEqual(test_company_2.get('address_1'), get_result_2.address_1)
        self.assertEqual(test_company_2.get('address_2'), get_result_2.address_2)
        self.assertEqual(test_company_2.get('city'), get_result_2.city)
        self.assertEqual(test_company_2.get('province'), get_result_2.province)
        self.assertEqual(test_company_2.get('zipcode'), get_result_2.zipcode)
        self.assertEqual(test_company_2.get('country'), get_result_2.country)
        self.assertEqual(test_company_2.get('phone'), get_result_2.phone)


if __name__ == '__main__':
    unittest.main()
