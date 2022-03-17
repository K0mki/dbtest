import sys
import psycopg2
import yaml
import argparse


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
    conn.commit()

    return print("PHONE BOOK UPDATED")

def search_contacts(search_term):
    '''
    search contact by search_term, search term can be any part of first, or last name or phone 
    '''
    conn = get_connection()
    curr = conn.cursor()

    conn.commit()

def all_contacts(order_by):
    '''
    return all contact ordered by order_by (id,fist_ame,last_n,pa cak i phone_n..)
    '''    
    conn = get_connection()
    curr = conn.cursor()
    curr.execute('SELECT id, first_name, last_name, phone_number FROM addressbook ORDER BY %s'%order_by) 
    all = curr.fetchall()
    for c in all:
        print(f'{c[0]:>5} {c[1]:<30} {c[2]:<30} {c[3]}')
             
        
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

    if len(sys.argv)<2:
        print('usage pytho3 ab.py command [param1] [param2] [param3]')
        print('commands')
        print('		-l, --list-all [order-by=first_name] show all contats')
        print('		-a, --add {fname} {lname} {phone}    add person')
        print('		-d, --delete {id}                    remove person by id')
        print('		-s, --search {term}                  search by term')
        print('')
        sys.exit()

    if sys.argv[1] in ('-l','--list-all'):
        all_contacts('first_name')
        sys.exit()

    if sys.argv[1] in ('-a','--add'):
        if len(sys.argv)!=5:
            print('usage pytho3 ab.py -a fname lname phone')
            sys.exit()
        contact=add_contact(sys.argv[2],sys.argv[3],sys.argv[4])
        print('id=',contact)
        

    # remove_contact(38)
    # update_contact( 'Mario','Mariooo', '065613131231', 30)
    contact=add_contact('Ana2', 'Anic', '0651234576')
    # print(contact)   
    # contacts=all_contacts('first_name')
    # print(contacts)
    




    # parser = argparse.ArgumentParser()
    # parser.add_argument("--help", help="help")
    # parser.add_argument("--all", help="print more details what you do", action="store_true")
    # parser.add_argument("--search", help="", )
    # parser.add_argument("--add", help="", )
    # parser.add_argument("--delete", help="", )
    # parser.add_argument("--update", help="brisanje", )
    '''
    sa argparse bib liotekom napravi sledec komande
    
    
        ./ab.py --help
        ./ab.py --all
            lista sve iz baze sortirane po first name-u
        ./ab.py --search term
            lista sve koji match-uju taj search term
        ./ab.py --add --first_name=pera --last_name=detlic --phon_number=123123
            dodaje i vraca id doatog
        ./ab.py --delete id
            briise sa tim id-om
            
        ./ab.py --update --id=xxx --first_name=pera --last_name=detlic --phon_number=12313
        
        
    '''    