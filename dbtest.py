import psycopg2
import psycopg2.extras


hostname="localhost"
database="test"
username="stefan1"
pwd="admin"
port_id = 5432

con= None
cur= None

if __name__=='__main__':

    
    try:
        conn = psycopg2.connect(
            host = hostname,
            dbname = database,
            user = username, 
            password = pwd,
            port = port_id
            )
    
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute('DROP TABLE IF EXISTS zaposleni')
    
        create_script= '''CREATE TABLE zaposleni(
                                id  int PRIMARY KEY,
                                ime varchar(40) NOT NULL,
                                plata int,
                                dept_id varchar(30))'''
    
        cur.execute(create_script)
    
        insert_script = 'INSERT INTO zaposleni (id, ime, plata, dept_id) VALUES(%s, %s, %s, %s)'
        insert_values = [(1, 'Marko', 50000,'D1' ), (2, 'Darko',55000, 'D2'),(3,'Zoran',70000,'D1')]
        for record in insert_values:
            cur.execute(insert_script, record)
    
        update_script='UPDATE zaposleni SET plata= plata+(plata*0.1)'
        cur.execute(update_script)
        
        cur.execute('SELECT * FROM zaposleni')
        for record in cur.fetchall():
            print(record['ime'],record['plata'])
        
    
    
        conn.commit()
    
    
        
    except Exception as error:
        print(error)
    finally: 
        if cur is not None :
            cur.close()
        if con is not None :
            conn.close()