import unittest
import adr

#python -m unittest test_adr.py

class TestAddContact(unittest.TestCase):
    def test_add(self):
        self.assertEqual(adr.add_contact('Stefan','Kotarac','1234','Mobile','True','Moj broj'), 'Stefan Kotarac 1234 Mobile t Moj broj')


if __name__ == '__main__':
    unittest.main()
