import unittest
import functions
from models import *

class TestAddContact(unittest.TestCase):
    def test_add_contact(self):
        self.assertEqual(functions.add_contact("Stefan","Kotarac","0615855790","mobile","True","Moj Broj"),'Added contact')
        
#     def test_add_contact(self):
#         self.assertEqual(functions.add_contact())
#     def test_add_contact(self):
#         self.assertEqual(functions.add_contact())

    def test_add_number(self):
        c1 = Contact(first_name ='Stefan', last_name = 'Kotarac')
        p1 = PhoneNumber( phone_number = '12345678', phone_type = 'mobile' , is_primary = 'True', contact_id = c1.id, note = "Moj broj" )
        self.assertEqual(functions.add_number(c1.id, '23456', 'work' , "dsadsadsa" , 'test br 2'),"Added number")
#     def test_add_number(self):
#         self.assertEqual(functions.add_number())
#     def test_add_number(self):
#         self.assertEqual(functions.add_number())

    def test_remove_contact(self):
        c1 = Contact(first_name ='Stefan', last_name = 'Kotarac')
        p1 = PhoneNumber( phone_number = '12345678', phone_type = 'mobile' , is_primary = 'True', contact_id = c1.id, note = "Moj broj" )
        self.assertEqual(functions.remove_contact('first_name','Stefan'),'Removed contact')
#     def test_remove_contact(self):
#         self.assertEqual(functions.remove_contact())
#     def test_remove_contact(self):
#         self.assertEqual(functions.remove_contact())

#     def test_update_contact(self):
#         self.assertEqual(functions.update_contact())
#     def test_update_contact(self):
#         self.assertEqual(functions.update_contact())
#     def test_update_contact(self):
#         self.assertEqual(functions.update_contact())

#     def test_search_contacts(self):
#         self.assertEqual(functions.search_contacts())
#     def test_search_contacts(self):
#         self.assertEqual(functions.search_contacts())
#     def test_search_contacts(self):
#         self.assertEqual(functions.search_contacts())

#     def test_detailed_contact(self):
#         self.assertEqual(functions.detailed_contact())
#     def test_detailed_contact(self):
#         self.assertEqual(functions.detailed_contact())
#     def test_detailed_contact(self):
#         self.assertEqual(functions.detailed_contact())
        
#     def test_all_contacts(self):
#         self.assertEqual(functions.all_contacts())
#     def test_all_contacts(self):
#         self.assertEqual(functions.all_contacts())   
#     def test_all_contacts(self):
#         self.assertEqual(functions.all_contacts())
if __name__ == '__main__':
    unittest.main()
