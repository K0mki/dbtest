#!.venv/bin/python
from tortoise import Tortoise, run_async, fields 
from tortoise.models import Model 
import uuid
import sys
import argparse 




class PhoneTypes(Model):
    phone_types = fields.TextField(10)

    class Meta:
        table= "phone_types"
    
    def __str__(self):
        return f"{self.phone_types}"

# PhoneTypes_Pydantic = pydantic_model_creator(PhoneTypes, name="Contacts" )
# PhoneTypesIn_Pydantic = pydantic_model_creator (PhoneTypes, name="ContactsIn", exclude_readonly=True)

class Contacts(Model):
    id = fields.IntField(pk=True)
    first_name = fields.TextField()
    last_name = fields.IntField()

    class Meta:
        table= "contacts"
    
    def __str__(self):
        return f"{self.id}, {self.first_name}, {self.last_name}" 

# Contacts_Pydantic = pydantic_model_creator(Contacts, name="Contacts" )
# ContactsIn_Pydantic = pydantic_model_creator (Contacts, name="ContactsIn", exclude_readonly=True)

class PhoneNumbers(Model):
    id = fields.IntField(pk = True)
    contacts_id = fields.IntField
    is_primary = fields.BooleanField()
    phone_number = fields.TextField
    phone_type = fields.TextField
    note = fields.TextField

    class Meta:
        table= "phone_numbers"
    
    def __str__(self):
        return f"{self.id}, {self.contacts_id}, {self.is_primary}, {self.phone_number}, {self.phone_type}, {self.note}"

# PhoneNumbers_Pydantic = pydantic_model_creator(PhoneNumbers, name="PhoneNumbers")
# PhoneNumbersIn_Pydantic = pydantic_model_creator(PhoneNumbers, name="PhoneNumbersIn", exclude_readonly=True)

async def add_contact(first_name, last_name, phone_number, phone_type, is_primary, note):     #-a
    '''
        Add contact
    '''
    id   = uuid.uuid4()   # CONTACT ID
    id_p = uuid.uuid4()   # PHONE ID
    is_primary = 'true' if is_primary in (True, 1, 'True' , 'true' , 'yes' , 'da' , '1' ) else 'false'
    
    contact = Contacts(id = id, first_name=first_name, last_name=last_name)
    contact = PhoneNumbers (id = id , contacts_id = id_p , phone_number = phone_number, phone_type = phone_type, is_primary = is_primary, note = note)

    
    await contact.save()

async def add_number(contacts_id, phone_number, phone_type, is_primary, note):
    '''
        Add another phone number to existing contact
    '''
    is_primary = True if is_primary in (True, 1, 'true','yes','da','1') else 'false'
    id_p = uuid.uuid4()   # PHONE ID
    number = PhoneNumbers (id = id_p , contacts_id = contacts_id , phone_number = phone_number, phone_type = phone_type, is_primary = is_primary, note = note)

    await number.save()

async def remove_contact(id):
    '''
        Remove contact connected to provided ID
    '''
    await Contacts.filter(id=id).delete()


async def update_contact(id, update, value):
    '''
        Update contact
    '''
    # a = 'Contacts' if update in ('first_name','last_name') else 'PhoneNumbers'
    # id1= 'id' if a in('contacts') else 'contacts_id'
    if update in ('first_name','last_name'):
        await Contacts.filter(id = id).update(update=value)
    else:
        await PhoneNumbers.filter(contacts_id = id).update(update=value)
    '''
        Update contact
    '''

async def search_contacts(search_term , what): 
    '''
        Search for contacts by search_term, search term can be id, first_name, last_name or phone_number, then print it out
    '''
    # search_list = [(x.username, x.age) for x in await User.filter().all()]
    # return search_list
    
    contact = await Contacts.filter(search_term = what).all()

    return await contact

async def detailed_contact(id): 
    '''
        Show info for provided ID's contact
    '''
    

async def all_contacts(order_by, direction): 
    '''
        Return all contact ordered by order_by (id,fist_name,last_name,phone_number)
    '''    
    all = await Contacts.all(), PhoneNumbers.all() #??
    for a in all:
        await print(f"{a[0]:<35} | {a[1]+' '+a[2]:^25} | {a[3]:<12} {a[4]:<6} {a[5]:>5} | {[6]}")

async def init():

    await Tortoise.init(
        db_url='postgres://ab.sql',
        modules={'models': ['adr']}
    )
    await Tortoise.generate_schemas()

async def ab():
    '''
        pytho3 ab.py [command] param1 param2 param3 ... [params zavise od komande]
    '''

    parser= argparse.ArgumentParser(description='Edit addressbook contacts')

    parser.add_argument('-a', '--add', metavar=('[first name]','[last name]','[phone_number]','[phone_type]', '[is_primary]', '[note]'), help='Add a contact', nargs=6)
    parser.add_argument('-n', '--number', metavar=('[contacts_id]','[phone_number]','[phone_type]','[is_primary]','[note]'), help='Add a phone to a contact', nargs=5)
    parser.add_argument('-r', '--remove', metavar='[id]', help='Remove a contact by ID', nargs=1)
    parser.add_argument('-u', '--update', metavar=('[id]', '[update]','[value]'), help='Update contact', nargs=3)
    parser.add_argument('-s', '--search', metavar='[first_name / last_name / phone/number / id]', help='Search and print all contacts containing provided term', nargs=1)
    parser.add_argument('-d', '--details', metavar='[id]', help='Show details about contact with provided id', nargs=1)
    parser.add_argument('-l', '--list-all', action='store_true', help='Show all contacts, sorted by provided arguments') # metavar=('[-o / -d]') ?

    parser.add_argument('--sort',  help='Chose sorting parameter', default='first_name', choices=['first_name','last_name','phone_number','id'])
    parser.add_argument('--direction', help='Chose sorting direction', default='asc', choices=['asc','desc'])

    args=parser.parse_args()

    if args.add:                #Add contact
        add_contact(*args.add)
        return True

    if args.number:             #Add number
        add_number(args.number[0],args.number[1],args.number[2],args.number[3],args.number[4])
        return True

    if args.remove:             #Remove contact 
        remove_contact(args.remove[0])    
        return True
    
    if args.update:             #Update contact
        update_contact(*args.update)
        return True

    if args.search:             #Search contact
        search_contacts(*args.search, args.sort, args.direction)
        return True

    if args.details:            #Search specific user
        detailed_contact(args.details[0])
        return True

    if args.list_all:           #List contacts
        try:
            all_contacts(args.sort, args.direction)
        except Exception as e:
            print('Greska')
            return False
        
        return True
        
    print('Unknow command')
    return False
# run_async is a helper function to run simple async Tortoise scripts.
if __name__ == '__main__':

    if  not ab():
        sys.exit(1)
        
    sys.exit(0)


run_async(init())
