import unittest
import functions
from models import *

class TestAdr(unittest.TestCase):
    def test_setup(self):
        s = str(functions.setup())
        self.assertIn("daasup", s)

    # def test_set(self):
    #     self.assertEqual(functions.setup(),'Database created')

    # # def test_add(self):
    # #     self.assertEqual(functions.add_contact("Stefan","Kotarac","0615855790","mobile","True","Moj Broj"), 'Added contact')

    # def test_add_contact(self):
    #     a = str(functions.add_contact("Stefan","Kotarac","0615855790","mobile","True","Moj Broj"))
    #     self.assertIn('object add_contact', a)

    # def test_add_number(self):
    #     c1 = Contact(first_name ='Stefan', last_name = 'Kotarac')
    #     n = str(functions.add_number(c1.id, '23456', 'work' , "dsadsadsa" , 'test br 2'))
    #     self.assertIn("object add_number",n)

    # def test_remove_contact(self):
    #     c1 = Contact(first_name ='Stefan', last_name = 'Kotarac')
    #     r = str(functions.remove_contact('first_name','Stefan'))
    #     self.assertIn('object remove_contact',r)

    # def test_update_contact(self):
    #     c1 = Contact(first_name ='Stefan', last_name = 'Kotarac')
    #     u = str(functions.update_contact(c1.id, 'first_name','Testt'))
    #     self.assertIn("object update_contact",u)

    # def test_search_contacts(self):
    #     pass

    # def test_detailed_contact(self):
    #     pass

    # def test_all_contacts(self):
    #     pass

if __name__ == '__main__':
    unittest.main()
