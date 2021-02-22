CREATE TABLE public.order
(
    id serial PRIMARY KEY,
    name VARCHAR (50) NOT NULL,
    description VARCHAR NULL,
    created_on TIMESTAMP NOT NULL
);

CREATE TABLE public.events
(
    id serial PRIMARY KEY,
    json_object text NULL,
    occured_on TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);


CREATE OR REPLACE FUNCTION public.save_event() RETURNS trigger AS
$BODY$
BEGIN
    INSERT INTO
        public.events(json_object)
        VALUES(row_to_json(NEW));
    RETURN new;
END;
$BODY$
LANGUAGE 'plpgsql' VOLATILE COST 100;


CREATE TRIGGER order_after
AFTER INSERT
ON public.order
FOR EACH ROW
EXECUTE PROCEDURE public.save_event();