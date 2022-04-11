import argparse
import sys
from tortoise import Tortoise, connections
from tortoise.transactions import in_transaction
from models import * 

async def arg():
    '''
        python3 adr.py [command] param1 param2 param3 ... [params zavise od komande]
    '''
    await Tortoise.init(db_url="postgres://stefan:123@localhost:5432/adr" , modules={"models": ["__main__"]}) 

    parser = argparse.ArgumentParser(description='Edit addressbook contacts')

    parser.add_argument('-a', '--add',      metavar = ('[first_name]','[last_name]','[phone_number]','[phone_type]', '[is_primary]', '[note]'), help='Add a contact', nargs=6)
    parser.add_argument('-n', '--number',   metavar = ('[contacts_id]','[phone_number]','[phone_type]','[is_primary]','[note]'), help='Add aother phone number to a contact', nargs=5)
    parser.add_argument('-r', '--remove',   metavar = ('[what]' , '[where]'), help='Remove a contact', nargs=2)
    parser.add_argument('-u', '--update',   metavar = ('[id]', '[update]','[value]'), help='Update contact', nargs=3)
    parser.add_argument('-l', '--list-all', action='store_true', help='Show all contacts, sorted by provided arguments')
    parser.add_argument('-s', '--search',   metavar = ('[first_name / last_name / phone/number / id]'), help='Search and print all contacts containing provided term', nargs=1)
    parser.add_argument('-d', '--details',  metavar = ('[id]'), help='Show details about contact with provided id', nargs=1)

    # parser.add_argument('--setup',  help='Clear and create database',)
    # parser.add_argument('--sort',  help='Chose sorting parameter', default='first_name', choices=['first_name','last_name','phone_number','id'])
    # parser.add_argument('--direction', help='Chose sorting direction', default='asc', choices=['asc','desc'])


    args = parser.parse_args()

    if args.add:                #Add contact
        await add_contact(*args.add)
        return True

    if args.number:             #Add number
        await add_number(*args.number)
        return True

    if args.remove:             #Remove contact 
        await remove_contact(*args.remove)    
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

    # if args.setup:             #Setup database
    #     await setup()
    #     return True

    if args.list_all:           #List contacts
        try:
            await all_contacts(args.sort, args.direction)
        except Exception as e:
            await print('Greska')
            return False
        
        return True
print ('Setup and eddit your addressbook')

async def setup():
    await Tortoise.init(db_url="postgres://stefan:123@localhost:5432/adr" , modules={"models": ["__main__"]}) 
    await Tortoise.generate_schemas()

    mobile = await PhoneType.filter(name='Mobile').get_or_none()
    if not mobile:
        mobile = PhoneType(name="Mobile")
        await mobile.save()
    work = await PhoneType.filter(name='Work').get_or_none()
    if not work:
        work = PhoneType(name="Work")
        await work.save()
    home = await PhoneType.filter(name='Home').get_or_none()
    if not home:
        home = PhoneType(name="Home")
        await home.save()
    other = await PhoneType.filter(name='Other').get_or_none()
    if not other:
        other = PhoneType(name="Other")
        await other.save()

    c1 = Contact(first_name ='Stefan', last_name = 'Kotarac')
    await c1.save()
    p1 = PhoneNumber( phone_number = '12345678', phone_type = mobile , is_primary = 'True', contact_id = c1.id, note = "Moj broj" )
    p12 = PhoneNumber( phone_number = '23456789', phone_type = home , is_primary = False, contact_id = c1.id, note = "Kucni broj" )
    await p1.save()
    await p12.save()
    c2 = Contact(first_name ='Marko', last_name = 'Markovic')
    await c2.save()
    p2 = PhoneNumber( phone_number = '34567890', phone_type = mobile , is_primary = 'True', contact_id = c2.id, note = "Glavni broj" )
    await p2.save()

    await add_contact('Test', 'Test' , '1234', mobile , "da" , 'test br')
    await add_number(c2.id , '23456', work , "dsadsadsa" , 'test br 2')
    await remove_contact('first_name','Test')
    # await update_contact('341abf6c-0c66-4026-9eef-9901f10282d6', 'note', 'Moj glavni broj')
    # await search_contacts('first_name', 'Stefan')
    # await detailed_contact("341abf6c-0c66-4026-9eef-9901f10282d6") #??
    # await all_contacts("first_name", "desc")


async def add_contact(first_name, last_name, phone_number, p_type, is_primary, note):                   #-a
    '''
        Add contact
    '''
    is_primary =  is_primary in (True, 1, 'True' , 'true' , 'yes' , 'da' , '1' )
    note = '' if note in ('',' ') else note

    contact = Contact( first_name = first_name , last_name = last_name)  
    await contact.save()
    phone = PhoneNumber( phone_number = phone_number , phone_type = p_type , is_primary = is_primary , contact_id = contact.id ,note = note)
    await phone.save()

    return print('Added contact')

async def add_number(contact_id, phone_number, p_type, is_primary, note):                               #-n
    '''
        Add another phone number to existing contact
    '''
    is_primary =  is_primary in (True, 1, 'True' , 'true' , 'yes' , 'da' , '1' )
    note = '' if note in ('',' ') else note

    phone = PhoneNumber( phone_number = phone_number , phone_type = p_type , is_primary = is_primary , contact_id = contact_id ,note = note)
    await phone.save()
    return print('Added number')

async def remove_contact(where,what):                                                                    #-n
    '''
        Remove contact
    '''
    await Contact.filter(**{where:what}).delete()
    return print("Removed contact" )

async def update_contact(id, upd, value):                                                                #-u
    '''
        Update contact
    '''
    if upd in ('first_name' , 'last_name'):
        contact = await Contact.filter(id=id).update(**{upd:value})
    else:
        contact = await PhoneNumber.filter(contact_id=id).update(**{upd:value})
    await contact.save()

    return print('Contact Updated')

async def search_contacts(search_term , what):                                                #-s
    '''
        Search for contacts by search_term, search term can be id, first_name, last_name or phone_number, then print it out
    '''
    # search_list = [(x.username, x.age) for x in await User.filter().all()]
    # return search_list
    
    if search_term in ('first_name','last_name'):
       contact =  await Contact.filter(**{search_term:what}).all()
       print(contact)
    else:
       phone = await PhoneNumber.filter(**{search_term:what}).all()
       print(phone)


async def detailed_contact(id):                                                               #-d
    '''
        Show info for provided ID's contact
    '''
    
    contacts = await Contact.filter(id = id).prefetch_related('phone_numbers','phone_numbers__phone_type')
    for contact in contacts:
        print(contact)


async def all_contacts(order_by , direction):                                                           #-l
    '''
        Return all contact ordered by order_by (id,fist_name,last_name,phone_number)
    '''
    
    conn = connections.get("default")
    a = await conn.execute_query_dict('SELECT c.id, first_name, last_name, phone_number, phone_type_id, is_primary, note FROM contacts c LEFT JOIN phone_numbers p ON c.id = p.contact_id where p.is_primary=true ORDER BY %s %s ' %(order_by, direction))  
    print(a)
    # rows = conn.all()
    # for r in rows:
    #     print(f"{r[0]:<35} | {r[1]+' '+r[2]:^25} | {r[3]:<12} {r[4]:<6} {r[5]:>5} | {r[6]}")

