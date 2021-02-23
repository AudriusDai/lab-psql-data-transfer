# lab-psql-data-transfer
PoC for transferring data. It's based on trigger that might act on Update/Insert/Delete and populate the job to another table called `job_queue`. Jobs are constantly being pulled by some python worker.

For local setup you'll have to have a docker installed. Run these commands on root level:
```
docker-compose up

# or --build for force rebuild the images
docker-compose up --build
```
Destroy setup:
```
docker-compose down
```

For connecting to db go to docker container of db & paste the commands:
```
> psql -h db -U username -d database
> Password for user username: 
> secret
```
Write queries i.e.:
```
database=# select * from public.job_queue;
```
# Functionality
[postgres](postgres) - runs database with migrations scripts. Migration contains tables, trigger which populates the job to separate table & function for reading jobs.

[publisher](publisher) - connects to db and does the INSERT to table periodically.

[listener](listener) - connects to db and pulls the data from the jobs table.

It should be fail-safe. By that you can turn off listener and turn back again - the listener will continue it's job.

If job is stuck for more than 5 minutes, then Listener is going to pick it up again.

# Cons
- Listener is using polling mechanism every amount of time set. Not that efficient as Notify/Listen (pub/sub) approach.
