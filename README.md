# lab-psql-data-transfer
PoC for transferring data. It's based on trigger that might act on Update/Insert/Delete and populate the event to another table called `events`. Events are constantly being pulled by some python worker.

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

# Functionality
[postgres](postgres) - runs database with migrations scripts. Migration contains tables and trigger which populates the event to separate table.

[publisher](publisher) - connects to db and does the INSERT to table periodically.

[listener](listener) - connects to db and pulls the data from the events table. It should contain it's own data regarding latest handled records.

It should be fail-safe. By that you can turn off listener and turn back again - the listener will continue it's job.

# Cons
- Listener is using polling mechanism every amount of time set. Not that efficient as Notify/Listen (pub/sub) approach.