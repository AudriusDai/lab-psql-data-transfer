
import time
import psycopg2

print('Starting publisher!')
time.sleep(3)  # workaround alert! need to wait for db to bootup

db_name = 'database'
db_user = 'username'
db_pass = 'secret'
db_host = 'db'
db_port = '5432'

try:
    print('Connecting to db.')
    connection = psycopg2.connect(user=db_user,
        password=db_pass,
        host=db_host,
        port=db_port,
        database=db_name)
    cursor = connection.cursor()

    print('Working..')
    while True:
        cursor.execute(f"INSERT INTO public.order(name, description, created_on) VALUES ('The name', 'Description it is!', '2004-10-19 10:23:54')")
        connection.commit()
        print('Record inserted.')
        time.sleep(0.5)
finally:
    if(connection):
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")
    