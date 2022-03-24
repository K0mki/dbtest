DROP TABLE IF EXISTS phone_numbers;
DROP TABLE IF EXISTS contacts;
DROP TABLE IF EXISTS lookup_phone_types;

CREATE TABLE lookup_phone_types(
    phone_types VARCHAR(32) PRIMARY KEY
);

CREATE TABLE contacts(
    id UUID PRIMARY KEY ,
    first_name VARCHAR(128) NOT NULL,
    last_name VARCHAR(128)
);

CREATE TABLE phone_numbers(
    id UUID PRIMARY KEY,
    contacts_id UUID,
    is_primary BOOLEAN DEFAULT NULL,
    phone_number VARCHAR(128),
    phone_type VARCHAR(32),
    note TEXT DEFAULT NULL,
    
    UNIQUE ( contacts_id,is_primary)
);


ALTER TABLE phone_numbers ADD CONSTRAINT "contact_constraint" FOREIGN KEY(contacts_id) REFERENCES contacts(id) ON DELETE CASCADE;
ALTER TABLE phone_numbers ADD CONSTRAINT "phone_type_constraint" FOREIGN KEY(phone_type) REFERENCES lookup_phone_types(phone_types)ON DELETE CASCADE;

--ALTER TABLE links ADD CONSTRAINT "type_constraint"
--FOREIGN KEY (type) REFERENCES links_type_lookup (name); 

INSERT INTO lookup_phone_types (phone_types) VALUES ('Mobile');
INSERT INTO lookup_phone_types (phone_types) VALUES ('Home');
INSERT INTO lookup_phone_types (phone_types) VALUES ('Work');
INSERT INTO lookup_phone_types (phone_types) VALUES ('Other');


--!
--!INSERT INTO contacts (id, first_name, last_name) VALUES ('962249dc-c8ff-45b6-a937-a23c8d78bbfb','Stefan','Kotarac');
--!
--!INSERT INTO phone_numbers (id, contacts_id, phone_type, phone_number, is_primary, note) VALUES ('f682ba62-abc8-4bc6-885b-f2d866d4cfaa','962249dc-c8ff-45b6-a937-a23c8d78bbfb','Mobile','0615855790',true,'Zvati do 23h');
--!
--!INSERT INTO contacts (id, first_name, last_name) VALUES ('f73142b2-a6d9-4b7c-a932-c4403ae7e88a','Igor','Jeremic');
--!
--!INSERT INTO phone_numbers (id, contacts_id, phone_type, phone_number, is_primary, note) VALUES ('95dd7bbe-c32e-47c2-b107-5c19d6470a15','f73142b2-a6d9-4b7c-a932-c4403ae7e88a','Mobile','0695967576',true,NULL);
--!INSERT INTO phone_numbers (id, contacts_id, phone_type, phone_number, is_primary, note) VALUES ('bb9f251b-06e6-4ee0-b07e-cb1421f8b168','f73142b2-a6d9-4b7c-a932-c4403ae7e88a','Home','0112121212',false,NULL);
--!
--!INSERT INTO contacts (id, first_name, last_name) VALUES ('f9137614-ec26-4309-8450-9efc820e94eb', 'Marko', 'Markovic');
--!
--!INSERT INTO phone_numbers (id, contacts_id, phone_type, phone_number, is_primary, note) VALUES ('4edc1270-6b13-4eed-89fc-7ead1f29b18c','f9137614-ec26-4309-8450-9efc820e94eb','Mobile','0611234567',true,'Zvati posle 17h');
--!INSERT INTO phone_numbers (id, contacts_id, phone_type, phone_number, is_primary, note) VALUES ('b517ee21-dfed-4f5e-8c2f-35d9becd2faf','f9137614-ec26-4309-8450-9efc820e94eb','Work','0621234567',false,'Zvati do 17h');
--!INSERT INTO phone_numbers (id, contacts_id, phone_type, phone_number, is_primary, note) VALUES ('4a8aab47-2ecc-40fd-bda0-35b99dd62576','f9137614-ec26-4309-8450-9efc820e94eb','Home','0631234567',false,'Zvati do 23h');
--!INSERT INTO phone_numbers (id, contacts_id, phone_type, phone_number, is_primary, note) VALUES ('19114e29-978e-4293-8b3e-453ecfc23302','f9137614-ec26-4309-8450-9efc820e94eb','Other','0641234567',false,'Zvati samo u hitnim slucajevima');
--!
--!--SELECT c.id, first_name, last_name, phone_number, note FROM contacts c INNER JOIN phone_numbers p ON c.id = p.contacts_id;
--!--=>
--!--                   id                  | first_name | last_name | phone_number |              note               
--!-- --------------------------------------+------------+-----------+--------------+---------------------------------
--!--  962249dc-c8ff-45b6-a937-a23c8d78bbfb | Stefan     | Kotarac   | 0615855790   | Zvati do 23h
--!--  f73142b2-a6d9-4b7c-a932-c4403ae7e88a | Igor       | Jeremic   | 0695967576   | 
--!--  f73142b2-a6d9-4b7c-a932-c4403ae7e88a | Igor       | Jeremic   | 0112121212   | 
--!--  f9137614-ec26-4309-8450-9efc820e94eb | Marko      | Markovic  | 0611234567   | Zvati posle 17h
--!--  f9137614-ec26-4309-8450-9efc820e94eb | Marko      | Markovic  | 0621234567   | Zvati do 17h
--!--  f9137614-ec26-4309-8450-9efc820e94eb | Marko      | Markovic  | 0631234567   | Zvati do 23h
--!--  f9137614-ec26-4309-8450-9efc820e94eb | Marko      | Markovic  | 064234567    | Zvati samo u hitnim slucajevima
--!
--!
--!-- select c.id, first_name, last_name, phone_number from contacts c left join phone_numbers p on p.contact_id=c.id where c.id='962249dc-c8ff-45b6-a937-a23c8d78bbfb';
--!
--!
--!-- select c.id, first_name, last_name, phone_number from contacts c left join phone_numbers p on p.contact_id=c.id where p.is_primary=true;
--!
--!-- select c.id, first_name, last_name, phone_type, phone_number from contacts c left join phone_numbers p on p.contact_id=c.id where p.is_primary=true;
--!
--!
--!-------------------------------------------------------------------------------------------------------------------------------------------
--!
--!
--!-- todo:
--!-- ne dozvoli da jedna osoba ima vise primarnih kontakta
--!--x-- napraviti lookup tabelu lookup_phone_types, napuniti je sa (mobile, home, business, satelite), i phone_type koristiti kao referencu u phone_number
--!-- 
--!-- napraviti funkcionalnst editovanja korisnika tako sto mu se doda, obrise ili izmeni broj
--!--    
--!-- izmena postojeceg
--!--    ./ab.py --update 962249dc-c8ff-45b6-a937-a23c8d78bbfb --phone-number f682ba62-abc8-4bc6-885b-f2d866d4cfaa 00000123
--!-- dodavanje novog
--!--    ./ab.py --update 962249dc-c8ff-45b6-a937-a23c8d78bbfb --add-phone-number 00000123
--!