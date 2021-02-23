
import time
import psycopg2

print('Starting publisher!')
time.sleep(4)  # workaround alert! need to wait for db to bootup
db_name, db_user, db_pass, db_host, db_port = ('database', 'username', 'secret', 'db', '5432')
try:
    print('Connecting to db.')
    connection = psycopg2.connect(user=db_user,
        password=db_pass,
        host=db_host,
        port=db_port,
        database=db_name)
    cursor = connection.cursor()

    print('Working on 10k inserts..')
    for x in range(10_000):
        cursor.execute(f"INSERT INTO public.order(name, description, created_on) VALUES ('The name', 'Description it is!', CURRENT_TIMESTAMP);")
        connection.commit()
    print('Records inserted.')
finally:
    if(connection):
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")
    