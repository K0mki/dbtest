import argparse
from cgitb import lookup
import sys
from unicodedata import name
from tortoise import Tortoise, connections
from models import * 
import subprocess

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
    parser.add_argument('-s', '--search',   metavar = ('[first_name / last_name / phone/number / id]'), help='Search and print all contacts containing provided term', nargs=2)
    parser.add_argument('-d', '--details',  metavar = ('[id]'), help='Show details about contact with provided id', nargs=1)

    parser.add_argument('--setup', action='store_true' ,  help='Clear and create database',)

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
        await update_contact(*args.update)
        return True

    if args.search:             #Search contact
        await search_contacts(*args.search)
        return True

    if args.details:            #Search specific user
        await detailed_contact(args.details[0])
        return True

    if args.setup:             #Setup database
        await setup()
        return True

    if args.list_all:           #List contacts
        await all_contacts()
        return True
    

async def setup():
    subprocess.call("./setup.sh")

    await Tortoise.init(db_url="postgres://stefan:123@localhost:5432/adr" , modules={"models": ["__main__"]}) 
    await Tortoise.generate_schemas()


    lookups =  {'phone_types':{}}
    
    for pt_name in ('Mobile','Work','Home','Other'):
        pt = await PhoneType.filter(name=pt_name).get_or_none()
        if not pt:
            pt = PhoneType(name=pt_name)
            await pt.save()    
        
        lookups['phone_types'][pt_name]=pt


    c1 = Contact(first_name ='Stefan', last_name = 'Kotarac')
    await c1.save()
    p1 = PhoneNumber( phone_number = '12345678', phone_type = lookups['phone_types']['Mobile'] , is_primary = 'True', contact_id = c1.id, note = "Moj broj" )
    p12 = PhoneNumber( phone_number = '23456789', phone_type = lookups['phone_types']['Work'] , is_primary = False, contact_id = c1.id, note = "Kucni broj" )
    await p1.save()
    await p12.save()
    c2 = Contact(first_name ='Marko', last_name = 'Markovic')
    await c2.save()
    p2 = PhoneNumber( phone_number = '34567890', phone_type = lookups['phone_types']['Work'] , is_primary = 'True', contact_id = c2.id, note = "Glavni broj" )
    await p2.save()

    return print ("Database created") 

async def add_contact(first_name, last_name, phone_number, p_type, is_primary, note):                   #-a
    '''
        Add contact
    '''
    lookups =  {'phone_types':{}}
    
    for pt_name in ('Mobile','Work','Home','Other'):
        pt = await PhoneType.filter(name=pt_name).get_or_none()
        if not pt:
            pt = PhoneType(name=pt_name)
            await pt.save()    
        
        lookups['phone_types'][pt_name]=pt
    
    is_primary =  is_primary in (True, 1, 'True' , 'true' , 'yes' , 'da' , '1' )
    note = '' if note in ('',' ') else note
    p = p_type.upper()
    contact = Contact( first_name = first_name , last_name = last_name)  
    await contact.save()
    phone = PhoneNumber( phone_number = phone_number , phone_type = lookups['phone_types'][p_type.capitalize()] , is_primary = is_primary , contact_id = contact.id ,note = note)
    await phone.save()

    return print('Added contact')

async def add_number(contact_id, phone_number, p_type, is_primary, note):                               #-n
    '''
        Add another phone number to existing contact
    '''
    is_primary =  is_primary in (True, 1, 'True' , 'true' , 'yes' , 'da' , '1' )
    
    note = '' if note in ('',' ') else note
    lookups =  {'phone_types':{}}
    
    
    for pt_name in ('Mobile','Work','Home','Other'):
        pt = await PhoneType.filter(name=pt_name).get_or_none()
        if not pt:
            pt = PhoneType(name=pt_name)
            await pt.save()    
        
        lookups['phone_types'][pt_name]=pt

    phone = PhoneNumber( phone_number = phone_number , phone_type = lookups['phone_types'][p_type.capitalize()] , is_primary = is_primary , contact_id = contact_id ,note = note)
    await phone.save()
    return print('Added number')

async def remove_contact(where,what):                                                                    #-n
    '''
        Remove contact
    '''
    if where in ('first_name' , 'last_name'):
        await Contact.filter(**{where:what}).delete()
    else:
        await PhoneNumber.filter(**{where:what}).delete()

    return print("Removed contact" )

async def update_contact(id, upd, value):                                                                #-u
    '''
        Update contact
    '''
    if upd in ('first_name' , 'last_name'):
        await Contact.filter(id=id).update(**{upd:value})
    else:
        await PhoneNumber.filter(id=id).update(**{upd:value})

    return print('Contact Updated')

async def search_contacts(what,search_term ):                                                            #-s
    '''
        Search for contacts by search_term, search term can be id, first_name, last_name or phone_number, then print it out
    '''
    contacts = await Contact.filter(**{search_term:what}).prefetch_related('phone','phone__phone_type')
    for contact in contacts:
        print(contact)

async def detailed_contact(id):                                                                           #-d
    '''
        Show info for provided ID's contact
    '''
    contacts = await Contact.filter(id = id).prefetch_related('phone','phone__phone_type')
    for contact in contacts:
        print(contact)


async def all_contacts():                                                                                #-l
    '''
        Return all contact ordered by order_by (id,fist_name,last_name,phone_number)
    '''
    
    contacts = await Contact.all().prefetch_related('phone','phone__phone_type')
    for contact in contacts:
        print(contact)

