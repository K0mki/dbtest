#!.venv/bin/python
import sys
import psycopg2
import yaml
import argparse 
import uuid

connection_cache = None

def get_connection():
    '''
        Create or return cached connection
    '''
    global connection_cache
    
    if connection_cache:
        return connection_cache
    
    with open('config.yaml') as f:
        config = yaml.safe_load(f)
    
    connection_cache = psycopg2.connect(**config['db'])
    return connection_cache

'''contacts c LEFT JOIN phone_numbers p ON c.id = p.contacts_id'''

id = uuid.uuid4()   # CONTACT
id_p = uuid.uuid4() # PHONE ID

def add_contact(first_name, last_name, phone_number, phone_type, is_primary, note):
    '''
        Add contact
    '''
    conn = get_connection()
    curr = conn.cursor()
    global id, id_p
    curr.execute(f"INSERT INTO contacts (id, first_name, last_name) VALUES ('{id}','{first_name}','{last_name}')")
    curr.execute(f"INSERT INTO phone_numbers (id, contacts_id, phone_number, phone_type, is_primary, note) VALUES ('{id_p}','{id}','{phone_number}','{phone_type}','{is_primary}','{note}')")
    conn.commit()
    
    return print(f'Added contact ID "{id}"')

def add_number(contacts_id, phone_number, phone_type, is_primary, note):
    '''
        Add another phone number to existing contact
    '''
    # curr.execute(f"UPDATE phone_numbers SET phone_number = '{phone_number}', phone_type = '{phone_type}', is_primary = '{is_primary}', note = '{note}' WHERE contacts_id = '{contacts_id}'")
    conn = get_connection()
    curr = conn.cursor()
    global id_p
    curr.execute(f"INSERT INTO phone_numbers (id, contacts_id, phone_number, phone_type, is_primary, note) VALUES ('{id_p}','{contacts_id}','{phone_number}','{phone_type}','{is_primary}','{note}')")
    # if {is_primary} == True :
    #     print("Dva glavna telefona!")
    #     sys.exit(0)
    # else : conn.commit()
    conn.commit()
    return print(f'Contact ID {contacts_id} phone updated')

def remove_contact(id):
    '''
        Remove contact connected to provided ID
    '''
    conn = get_connection()
    curr = conn.cursor()
    curr.execute(f"DELETE FROM contacts WHERE id = '{id}'")
    conn.commit()

    return print(f"Removed contact ID {id}")

def update_contact(first_name, last_name, phone_number, id):
    '''
        Update contact
    '''
    conn = get_connection()
    curr = conn.cursor()
    curr.execute(f"UPDATE addressbook SET first_name = '{first_name}' , last_name = '{last_name}' , phone_number = '{phone_number}' WHERE id = {id}")
    conn.commit()

    return print(f"Contact #{id} updated!")

def search_contacts(search_term):
    '''
        Search for contact by search_term, search term can be id, first_name, last_name or phone_number, then print it out
    '''
    conn = get_connection()
    curr = conn.cursor()
    curr.execute(f"SELECT * FROM addressbook WHERE to_tsvector(first_name || ' ' || last_name || ' ' || phone_number) @@ to_tsquery('{search_term}')") 
    rows = curr.fetchall()
    for r in rows:
        print(f"{r[0]:>5} {r[1]:<15} {r[2]:<20} {r[3]}")

def detailed_contact(id):
    '''
        Show info for provided ID's contact
    '''
    conn = get_connection()
    curr = conn.cursor()
    curr.execute(f"SELECT c.id, first_name, last_name, phone_number, is_primary, phone_type, note FROM contacts c LEFT JOIN phone_numbers p ON c.id = p.contacts_id WHERE c.id='{id}'")
    c = curr.fetchone()

    print('ID             :',c[0])
    print('Ime            :',c[1])
    print('Prezime        :',c[2])
    print('Telefon        :',c[3])
    if c[4] == True:
        print("Glavni telefon") 
    else:
         print("Nije glavni telefon")
    print('Vrsta telefona :',c[5])
    print('Poruka         :',c[6])

    '''
./ab.py -t 1

id      : 1
ime     : igor
prezime : jeremic
telefon : 0695967576


==>

id: .
ime: .
prezime: .
telefoni:	
    mobilni: 0695967576	(primarni)
    fiksni: 011123123
    poslovni: 011231231 


--verbose

id: .
ime: .
prezime: .
telefoni:       
    mobilni: 0695967576 (primarni)		(id=bb9f251b-06e6-4ee0-b07e-cb1421f8b168)..
    fiksni: 011123123				..
    poslovni: 011231231 			..


'''
    
#    for r in rows:
#        
#        print(f"{r[0]:>5} {r[1]:<15} {r[2]:<20} {r[3]}")
    

def all_contacts(order_by, direction):
    '''
        Return all contact ordered by order_by (id,fist_name,last_name,phone_number)
    '''    
    
    if order_by not in ('id','first_name','last_name','phone_number'):
        raise NameError('invalid order by')
    
    conn = get_connection()
    curr = conn.cursor()
    curr.execute(f'SELECT c.id, first_name, last_name, phone_number, phone_type, is_primary, note FROM contacts c LEFT JOIN phone_numbers p ON c.id = p.contacts_id ORDER BY {order_by} {direction}') 

    rows = curr.fetchall()
    for r in rows:
        print(f"{r[0]:>5} {r[1]:<15} {r[2]:<20} {r[3]}")

if __name__=='__main__':

    '''
        pytho3 ab.py [command] param1 param2 param3 ... [params zavise od komande]
    '''

    parser= argparse.ArgumentParser(description='Edit addressbook contacts')

    parser.add_argument('-a', '--add', metavar=('[first name]','[last name]','[phone_number]','[phone_type]', '[is_primary]', '[note]'), help='Add a contact', nargs=6)
   # parser.add_argument('-n', '--number', metavar=('[contacts_id]','[phone_number]','[phone_type]','[is_primary]','[note]'), help='Add a phone to a contact', nargs=5)
    parser.add_argument('-r', '--remove', metavar='[id]', help='Remove a contact by ID', nargs=1)
    parser.add_argument('-u', '--update', metavar=('[first_name]', '[last_name]','[phone_number]','[id]'), help='Update contact', nargs=4)
    parser.add_argument('-s', '--search', metavar='[first_name / last_name / phone/number / id]', help='Search and print all contacts containing provided term', nargs=1)
    parser.add_argument('-t', '--details', metavar='[id]', help='Show details about contact with provided id', nargs=1)
    parser.add_argument('-l', '--list-all', action='store_true', help='Show all contacts, sorted by provided arguments') # metavar=('[-o / -d]') ?

    parser.add_argument('-o', '--sort',  help='Chose sorting parameter', default='first_name', choices=['first_name','last_name','phone_number','id'])
    parser.add_argument('-d', '--direction', help='Chose sorting direction', default='asc', choices=['asc','desc'])

    # parser.add_argument('-f', '--first_name', help='first_name')
    # parser.add_argument('-n', '--last_name', help='last_name')
    # parser.add_argument('-p', '--phone', help='phone')

    args=parser.parse_args()

    if args.add:                #Add contact
        add_contact(*args.add)
        sys.exit(0) 

    # if args.number:             #Add number
    #     add_number(args.number[0],args.number[1],args.number[2],args.number[3],args.number[4])
    #     sys.exit(0)

    if args.remove:             #Remove contact 
        remove_contact(args.remove[0])    
        sys.exit(0)
    
    if args.update:             #Update contact
        update_contact(*args.update)
        sys.exit(0)

    if args.search:             #Search contact
       search_contacts(args.search[0])
       sys.exit(0)

    if args.details:            #Search specific user
        detailed_contact(args.details[0])
        sys.exit(0)

    if args.list_all:           #List contacts
        try:
            all_contacts(args.sort, args.direction)
        except Exception as e:
            print(e)
            sys.exit(1)
        
        sys.exit(0)
        

    print('Unknow command')
    sys.exit(1)
