from textwrap import indent
import sys
import psycopg2
import yaml
import argparse
import sys


connection_cache = None

def get_connection():
    '''
        create or return cached connection
    '''
    global connection_cache
    
    if connection_cache:
        return connection_cache
    
    with open('config.yaml') as f:
        config = yaml.safe_load(f)
    
    connection_cache = psycopg2.connect(**config['db'])
    return connection_cache


def add_contact(first_name, last_name, phone):
    '''
    adding contact
    '''
    
    conn = get_connection()
    curr = conn.cursor()
    curr.execute('insert into addressbook (first_name,last_name,phone_number) values (%s,%s,%s) returning id', (first_name, last_name, phone))
    _id = curr.fetchone()[0]
    conn.commit()
    
    return _id

def update_contact(first_name, last_name, phone, id):
    '''update contact'''
    conn = get_connection()
    curr = conn.cursor()
    curr.execute('update addressbook set first_name = %s , last_name = %s , phone_number =  %s where id = %s',(first_name, last_name, phone, id))
    curr.commit()

    return print("PHONE BOOK UPDATED")

def search_contacts(search_term):
    '''
    search contact by search_term, search term can be any part of first, or last name or phone 
    '''
    conn = get_connection()
    curr = conn.cursor()

    conn.commit()

def all_contacts(order_by, direction):
    '''
    return all contact ordered by order_by (id,fist_ame,last_n,pa cak i phone_n..)
    '''    
    
    if order_by not in ('id','first_name','last_name','phone_number'):
        raise NameError('invalid order by')
    
    conn = get_connection()
    curr = conn.cursor()
    curr.execute(f'SELECT id, first_name, last_name, phone_number FROM addressbook ORDER BY {order_by} {direction}') 

    rows = curr.fetchall()
    for r in rows:
        print(f"{r[0]:>5} {r[1]:<15} {r[2]:<20} {r[3]}")
    
def remove_contact(id):
    '''
    remove added contact
    '''
    conn = get_connection()
    curr = conn.cursor()
    curr.execute('DELETE FROM addressbook WHERE id = %s'%id)
    conn.commit()

    return print("REMOVED CONTACT %s"%id)

if __name__=='__main__':

    '''
    pytho3 ab.py [command] param1 param2 param3 ... [ params zavise od komande]
    '''
    
    # print(contact)   
    # all_contacts('id')
    # # search_contacts
    parser= argparse.ArgumentParser(description='Edit addressbook contacts')

    parser.add_argument('-r','--remove', help='remove a contact by ID')
    parser.add_argument('-a', '--add', metavar=('first name', 'last name','phone number'),help='add a contact', nargs=3)
    parser.add_argument('-l', '--list-all', action='store_true', help='show all contacts, sorted by provided argument')
    parser.add_argument('-u', '--update', help='update contact')
    parser.add_argument('-s', '--search',  help='search my term')
    parser.add_argument('-o', '--sort',  help='.', default='first_name')
    parser.add_argument('-d', '--direction', help='.', default='asc', choices=['asc','desc'])
    

    parser.add_argument('-f', '--first_name', help='first_name')
    parser.add_argument('-n', '--last_name', help='last_name')
    parser.add_argument('-p', '--phone', help='phone')

    args=parser.parse_args()
       
    if args.add:    
        print('added id=',add_contact(*args.add))
        sys.exit(0)
    
    if args.list_all:
        try:
            all_contacts(args.sort, args.direction)
        except Exception as e:
            print(e)
            sys.exit(1)
            
        sys.exit(0)
        
    print('unknow command')
    sys.exit(1)

#    if sys.argv[1] in ('-l','--list-all'):
#        all_contacts('%s'%sys.argv[2])
#        sys.exit()
#    
#    if sys.argv[1] in ('-a','--add'):
#        # if len(sys.argv)!=5:
#        #     print('Syntax error, usage: python3 ab.py -a first_name last_name phone_number')
#        # else:
#        contact=add_contact(sys.argv[2],sys.argv[3],sys.argv[4])
#        print('id=',contact)
 #       sys.exit()
 #       
 #   
#    if sys.argv[1] in ('-r','--remove'):
#        remove_contact('%s'%sys.argv[2])
#        sys.exit()
#
#    if sys.argv[1] in ('-u','--update'):
#        if len(sys.argv)!=5:
#            print('Syntax error, usage: python3 ab.py -u first_name last_name phone_number ID')
#            sys.exit()
#        else:
#            update_contact(sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5])
#        sys.exit()
