DROP TABLE IF EXISTS phone_numbers;
DROP TABLE IF EXISTS contacts;

CREATE TABLE contacts(
    id UUID PRIMARY KEY,
    first_name VARCHAR(128) NOT NULL,
    last_name VARCHAR(128)
);

-- todo:
-- ne dozvoli da jedna osoba ima vise primarnih kontakta
-- napraviti lookup tabelu lookup_phone_types, napuniti je sa (mobile, home, business, satelite), i phone_type koristiti kao referencu u phone_number
-- 
-- napraviti funkcionalnst editovanja korisnika tako sto mu se doda, obrise ili izmeni broj
--    
-- izmena postojeceg
--    ./ab.py --update 962249dc-c8ff-45b6-a937-a23c8d78bbfb --phone-number f682ba62-abc8-4bc6-885b-f2d866d4cfaa 00000123
-- dodavanje novog
--    ./ab.py --update 962249dc-c8ff-45b6-a937-a23c8d78bbfb --add-phone-number 00000123

CREATE TABLE phone_numbers(
    id UUID PRIMARY KEY,
    contact_id UUID,        
    is_primary BOOLEAN default NULL,
    phone_number VARCHAR(128) NOT NULL,
    phone_type VARCHAR(32),
    note TEXT default NULL, 
    constraint fk_contact FOREIGN KEY(contact_id) REFERENCES contacts(id)
);

insert into contacts (id, first_name, last_name) values ('962249dc-c8ff-45b6-a937-a23c8d78bbfb','Stefan','Kotarac');

insert into phone_numbers (id, contact_id, phone_type, phone_number, is_primary, note) values ('f682ba62-abc8-4bc6-885b-f2d866d4cfaa','962249dc-c8ff-45b6-a937-a23c8d78bbfb','mobile','0615855790',true,'zvati do 23h');

insert into contacts (id, first_name, last_name) values ('f73142b2-a6d9-4b7c-a932-c4403ae7e88a','Igor','Jeremic');

insert into phone_numbers (id, contact_id, phone_type, phone_number, is_primary, note) values ('95dd7bbe-c32e-47c2-b107-5c19d6470a15','f73142b2-a6d9-4b7c-a932-c4403ae7e88a','mobile','0695967576',true,null);
insert into phone_numbers (id, contact_id, phone_type, phone_number, is_primary, note) values ('bb9f251b-06e6-4ee0-b07e-cb1421f8b168','f73142b2-a6d9-4b7c-a932-c4403ae7e88a','home','0112121212',false,null);




select c.id, first_name, last_name, phone_number from contacts c left join phone_numbers p on p.contact_id=c.id;

--                  id                  | first_name | last_name | phone_number 
-- --------------------------------------+------------+-----------+--------------
--  962249dc-c8ff-45b6-a937-a23c8d78bbfb | Stefan     | Kotarac   | 0615855790
--  f73142b2-a6d9-4b7c-a932-c4403ae7e88a | Igor       | Jeremic   | 0695967576
--  f73142b2-a6d9-4b7c-a932-c4403ae7e88a | Igor       | Jeremic   | 0112121212
-- (3 rows)

select c.id, first_name, last_name, phone_number from contacts c left join phone_numbers p on p.contact_id=c.id where c.id='962249dc-c8ff-45b6-a937-a23c8d78bbfb';


select c.id, first_name, last_name, phone_number from contacts c left join phone_numbers p on p.contact_id=c.id where p.is_primary=true;

select c.id, first_name, last_name, phone_type, phone_number from contacts c left join phone_numbers p on p.contact_id=c.id where p.is_primary=true;

