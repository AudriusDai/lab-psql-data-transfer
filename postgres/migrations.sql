CREATE TABLE public.order
(
    id serial PRIMARY KEY,
    name VARCHAR (50) NOT NULL,
    description VARCHAR NULL,
    created_on TIMESTAMP NOT NULL
);


CREATE TABLE public.job_queue
(
    id serial NOT NULL,
    new_data json NULL,
    old_data json NULL,
    status character varying,
    operation VARCHAR (50) NOT NULL,
    added_on timestamp without time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    started timestamp without time zone NULL,
    ended timestamp without time zone NULL,
    CONSTRAINT "job_queue_pkey" PRIMARY KEY (id)
);


CREATE OR REPLACE FUNCTION public.queue_job() RETURNS trigger AS
$BODY$
BEGIN
    /* todo: handle OLD & NEW for other TG_OP's types */
    INSERT INTO
        public.job_queue(new_data, old_data, operation, status)
        VALUES(row_to_json(NEW), null, TG_OP, 'new');
    RETURN new;
END;
$BODY$
LANGUAGE 'plpgsql' VOLATILE COST 100;


CREATE TRIGGER order_after
AFTER INSERT
ON public.order
FOR EACH ROW
EXECUTE PROCEDURE public.queue_job();


CREATE OR REPLACE FUNCTION public.job_queue_get_jobs(
    _num_jobs_to_get integer)
    RETURNS TABLE(
        id integer, 
        new_data json,
        old_data json, 
        status character varying,
        operation VARCHAR (50),
        added_on timestamp
        )
AS $BODY$
DECLARE _record record;
BEGIN
   FOR _record IN
        SELECT *
        FROM public.job_queue as JQ_S
        WHERE (JQ_S.status = 'new' and JQ_S.added_on < NOW()) 
            or (JQ_S.status = 'pickedup' and JQ_S.ended is NULL and DATE_PART('minute', CURRENT_TIMESTAMP - JQ_S.started) > 5)
        ORDER BY JQ_S.added_on
        LIMIT _num_jobs_to_get FOR UPDATE SKIP LOCKED
   LOOP
        UPDATE public.job_queue as JQ_U 
        SET (status, started) = ('pickedup', CURRENT_TIMESTAMP)
        WHERE JQ_U.id = _record.id;

        id :=  _record.id;
        new_data :=  _record.new_data;
        old_data :=  _record.old_data;
        status :=  _record.status;
        operation :=  _record.operation;
        added_on :=  _record.added_on;

        RETURN NEXT;
   END LOOP;
end
$BODY$
LANGUAGE 'plpgsql'