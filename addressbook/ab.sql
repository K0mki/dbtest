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

INSERT INTO lookup_phone_types (phone_types) VALUES ('Mobile');
INSERT INTO lookup_phone_types (phone_types) VALUES ('Home');
INSERT INTO lookup_phone_types (phone_types) VALUES ('Work');
INSERT INTO lookup_phone_types (phone_types) VALUES ('Other');
