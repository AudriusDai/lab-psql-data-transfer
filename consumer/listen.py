import time
import psycopg2

print('Starting listener!')
time.sleep(3) # workaround alert! need to wait for db to bootup

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

    # todo: query the latest fecthed timestamp to start from

    print('Getting the events..')
    while True:
        # todo: adjust the query by latest fetched event timestamp
        # todo: use the timestamp local variable to set after each iteration
        # todo: lock the read resources
        # todo: add more consumers than just one. Prove that lock works.
        cursor.execute('select * from public.events order by occured_on')
        events = cursor.fetchmany(5)
        for row in events:
            print(f'Got row {str(row)}')
        else:
            print('havent found records.. ')
        
        time.sleep(5)
finally:
    if(connection):
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")