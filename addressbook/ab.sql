DROP TABLE IF EXISTS addressbook;

CREATE TABLE addressbook(
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(128) NOT NULL,
    last_name VARCHAR(128) NOT NULL,
    phone_number VARCHAR(128) NOT NULL
);
