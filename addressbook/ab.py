import sys
import psycopg2
import yaml
import argparse 


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


def add_contact(first_name, last_name, phone_number):
    '''
        Add contact
    '''
    conn = get_connection()
    curr = conn.cursor()
    curr.execute(f"INSERT INTO addressbook (first_name, last_name, phone_number) VALUES ('{first_name}','{last_name}','{phone_number}') RETURNING id")
    _id = curr.fetchone()[0]
    conn.commit()
    
    return print('Added contact ID #',_id)

def remove_contact(id):
    '''
        Remove contact connected to provided ID
    '''
    conn = get_connection()
    curr = conn.cursor()
    curr.execute(f'DELETE FROM addressbook WHERE id = {id}')
    conn.commit()

    return print(f"Removed contact ID #{id}")

def update_contact(first_name, last_name, phone_number, id):
    '''
        Update contact
    '''
    conn = get_connection()
    curr = conn.cursor()
    curr.execute(f"UPDATE addressbook SET first_name = '{first_name}' , last_name = '{last_name}' , phone_number = '{phone_number}' WHERE id = {id}")
    conn.commit()

    return print("Contact #",id,"updated!")

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
    curr.execute('SELECT * FROM addressbook WHERE id=%s'%id)
    rows = curr.fetchall()
    for r in rows:
        print(f"{r[0]:>5} {r[1]:<15} {r[2]:<20} {r[3]}")
    

def all_contacts(order_by, direction):
    '''
        Return all contact ordered by order_by (id,fist_name,last_name,phone_number)
    '''    
    
    if order_by not in ('id','first_name','last_name','phone_number'):
        raise NameError('invalid order by')
    
    conn = get_connection()
    curr = conn.cursor()
    curr.execute(f'SELECT id, first_name, last_name, phone_number FROM addressbook ORDER BY {order_by} {direction}') 

    rows = curr.fetchall()
    for r in rows:
        print(f"{r[0]:>5} {r[1]:<15} {r[2]:<20} {r[3]}")

if __name__=='__main__':

    '''
        pytho3 ab.py [command] param1 param2 param3 ... [params zavise od komande]
    '''

    parser= argparse.ArgumentParser(description='Edit addressbook contacts')

    parser.add_argument('-a', '--add', metavar=('first name', 'last name','phone number'),help='add a contact', nargs=3)
    parser.add_argument('-r', '--remove', help='remove a contact by ID', nargs=1)
    parser.add_argument('-u', '--update', help='update contact', nargs=4)
    parser.add_argument('-s', '--search',  help='search by term', nargs=1)
    parser.add_argument('-t', '--details', help='show details about user for provided id', nargs=1)
    parser.add_argument('-l', '--list-all', action='store_true', help='show all contacts, sorted by provided argument')

    parser.add_argument('-o', '--sort',  help='Chose sorting parameter', default='first_name', choices=['first_name','last_name','phone_number','id'])
    parser.add_argument('-d', '--direction', help='Chose sorting direction', default='asc', choices=['asc','desc'])

    parser.add_argument('-f', '--first_name', help='first_name')
    parser.add_argument('-n', '--last_name', help='last_name')
    parser.add_argument('-p', '--phone', help='phone')

    args=parser.parse_args()

    if args.add:                #Add contact
        add_contact(args.add[0],args.add[1],args.add[2])
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
