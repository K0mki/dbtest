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

id   = uuid.uuid4()   # CONTACT ID
id_p = uuid.uuid4()   # PHONE ID

def add_contact(first_name, last_name, phone_number, phone_type, is_primary, note):
    '''
        Add contact
    '''
    is_primary = 'true' if is_primary in (True, 1, 'true','yes','da','1') else 'null'

    conn = get_connection()
    curr = conn.cursor()
    global id, id_p
    curr.execute("INSERT INTO contacts (id, first_name, last_name) VALUES (%s,%s,%s)", (str(id),first_name,last_name))
    curr.execute("INSERT INTO phone_numbers (id, contacts_id, phone_number, phone_type, is_primary, note) VALUES (%s,%s,%s,%s,%s,%s)",(str(id_p),str(id),phone_number,phone_type,is_primary,note))
    conn.commit()
    
    return print('Added contact ID',(str(id)))

def add_number(contacts_id, phone_number, phone_type, is_primary, note):
    '''
        Add another phone number to existing contact
    '''
    
    is_primary = True if is_primary in (True, 1, 'true','yes','da','1') else None
    
    conn = get_connection()
    curr = conn.cursor()
    global id_p
    
    curr.execute("INSERT INTO phone_numbers (id, contacts_id, phone_number, phone_type, is_primary, note) VALUES (%s,%s,%s,%s,%s,%s)" , (str(id_p),str(contacts_id),phone_number,phone_type,is_primary,note))
    conn.commit()
    return print('Contact ID %s phone added' %str(contacts_id))

def remove_contact(id):
    '''
        Remove contact connected to provided ID
    '''
    conn = get_connection()
    curr = conn.cursor()
    curr.execute("DELETE FROM contacts WHERE id = '%s'" %id)
    conn.commit()

    return print("Removed contact ID %s" %id)

def update_contact(first_name, last_name, phone_number, id):
    '''
        Update contact
    '''
    conn = get_connection()
    curr = conn.cursor()
    curr.execute("UPDATE contacts c LEFT JOIN phone_numbers p ON c.id = p.contacts_id SET first_name = '%s' , last_name = '%s' , phone_number = '%s' WHERE id = '%s'" %(first_name, last_name, phone_number, id))
    conn.commit()

    return print("Contact with ID %s updated!"%id)

def search_contacts(search_term):
    '''
        Search for contact by search_term, search term can be id, first_name, last_name or phone_number, then print it out
    '''
    conn = get_connection()
    curr = conn.cursor()
    curr.execute("SELECT * FROM contacts c LEFT JOIN phone_numbers p ON c.id = p.contacts_id WHERE to_tsvector(first_name || ' ' || last_name || ' ' || phone_number || ' ' || note) @@ to_tsquery('%s')" %search_term) 
    rows = curr.fetchall()
    for r in rows:
        print(f"{r[0]:<40} | {r[1]:<7} {r[2]:<7} | {r[3]:<12} | {r[5]:^5} {r[6]:<15} {r[7]:<10} | {r[8]:<20}")

def detailed_contact(id):
    '''
        Show info for provided ID's contact
    '''
    conn = get_connection()
    curr = conn.cursor()
    curr.execute("SELECT c.id, c.first_name, c.last_name, p.phone_number, p.is_primary, p.phone_type, p.note FROM contacts c LEFT JOIN phone_numbers p ON c.id = p.contacts_id WHERE c.id='%s' order by p.is_primary asc" %id)

    iter=0
    for i in curr.fetchall():
        if iter==0:
           print('ID       ',i[0])
           print('Ime      ',i[1])
           print('Prezime  ',i[2])
           print('-'*15)
        
        print('    tel:',i[3],f'({i[5]}) {"Glavni telefon" if i[4] else ""}', i[6])           

        iter+=1


def all_contacts(order_by, direction):
    '''
        Return all contact ordered by order_by (id,fist_name,last_name,phone_number)
    '''    

    
    conn = get_connection()
    curr = conn.cursor()
    curr.execute(f'SELECT c.id, first_name, last_name, phone_number, phone_type, is_primary, note FROM contacts c LEFT JOIN phone_numbers p ON c.id = p.contacts_id where p.is_primary=true ORDER BY {order_by} {direction}') 

    rows = curr.fetchall()
    for r in rows:
        print(f"{r[0]:<35} | {r[1]:^10} {r[2]:<10} | {r[3]:<12} {r[4]:<6} {r[5]:>5} | {r[6]}")

if __name__=='__main__':

    '''
        pytho3 ab.py [command] param1 param2 param3 ... [params zavise od komande]
    '''

    parser= argparse.ArgumentParser(description='Edit addressbook contacts')

    parser.add_argument('-a', '--add', metavar=('[first name]','[last name]','[phone_number]','[phone_type]', '[is_primary]', '[note]'), help='Add a contact', nargs=6)
    parser.add_argument('-n', '--number', metavar=('[contacts_id]','[phone_number]','[phone_type]','[is_primary]','[note]'), help='Add a phone to a contact', nargs=5)
    parser.add_argument('-r', '--remove', metavar='[id]', help='Remove a contact by ID', nargs=1)
    parser.add_argument('-u', '--update', metavar=('[first_name]', '[last_name]','[phone_number]','[id]'), help='Update contact', nargs=4)
    parser.add_argument('-s', '--search', metavar='[first_name / last_name / phone/number / id]', help='Search and print all contacts containing provided term', nargs=1)
    parser.add_argument('-t', '--details', metavar='[id]', help='Show details about contact with provided id', nargs=1)
    parser.add_argument('-l', '--list-all', action='store_true', help='Show all contacts, sorted by provided arguments') # metavar=('[-o / -d]') ?

    parser.add_argument('-o', '--sort',  help='Chose sorting parameter', default='first_name', choices=['first_name','last_name','phone_number','id'])
    parser.add_argument('-d', '--direction', help='Chose sorting direction', default='asc', choices=['asc','desc'])

    parser.add_argument('-f', '--first_name', help='first_name')
    parser.add_argument('-n', '--last_name', help='last_name')
    parser.add_argument('-p', '--phone', help='phone')
    parser.add_argument('-i', '--ID', help='id')

    args=parser.parse_args()

    if args.add:                #Add contact
        add_contact(*args.add)
        sys.exit(0) 

    if args.number:             #Add number
        add_number(*args.number)
        sys.exit(0)

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