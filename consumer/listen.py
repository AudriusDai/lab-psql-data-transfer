import time
import psycopg2

print('Starting listener!')
time.sleep(5) # workaround alert! need to wait for db to bootup
db_name, db_user, db_pass, db_host, db_port = ('database', 'username', 'secret', 'db', '5432')
pace = 500
try:
    print('Connecting to db.')
    connection = psycopg2.connect(user=db_user,
        password=db_pass,
        host=db_host,
        port=db_port,
        database=db_name)
    cursor = connection.cursor()
    print(f'Getting the jobs {pace} at the time..')
    while True:
        cursor.execute(f'select * from public.job_queue_get_jobs({pace});')
        jobs = cursor.fetchall()
        if not jobs:
            print('no jobs founds at the moment..')
        for row in jobs:
            print(f'Got row {str(row)}')
            cursor.execute(f"UPDATE public.job_queue SET status = 'done' WHERE id = {row[0]}")
        connection.commit()

        
        time.sleep(2)
finally:
    if(connection):
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")