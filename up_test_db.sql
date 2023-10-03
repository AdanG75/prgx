DROP DATABASE IF EXISTS pgrx_test;

CREATE DATABASE pgrx_test ENCODING UTF8;

-- Create Tables --

DROP TABLE IF EXISTS public.user CASCADE;

CREATE TABLE IF NOT EXISTS public.user (
    id serial NOT NULL,
    first_name character varying(80) NOT NULL,
    last_name character varying(80) NOT NULL,
    email character varying(80) UNIQUE NOT NULL,
    password character varying(65) NOT NULL,
    dropped boolean DEFAULT false NOT NULL
);

DROP TABLE IF EXISTS public.address CASCADE;

CREATE TABLE IF NOT EXISTS public.address (
    id serial NOT NULL,
    address_1 character varying(80) NOT NULL,
    address_2 character varying(80) NOT NULL,
    city character varying(80) NOT NULL,
    state character varying(80) NOT NULL,
    zip character varying(8) NOT NULL,
    country character varying(50) NOT NULL,
    dropped boolean DEFAULT false NOT NULL
);

DROP TABLE IF EXISTS public.user_address CASCADE;

CREATE TABLE IF NOT EXISTS public.user_address (
    id_user INTEGER,
    id_address INTEGER,
    valid boolean DEFAULT true NOT NULL
);

-- Create Constraints --

ALTER TABLE ONLY public.user
    ADD CONSTRAINT user_pkey PRIMARY KEY (id);

ALTER TABLE ONLY public.address
    ADD CONSTRAINT address_pkey PRIMARY KEY (id);

ALTER TABLE ONLY public.user_address
    ADD CONSTRAINT user_address_pkey PRIMARY KEY (id_user, id_address);

ALTER TABLE ONLY public.user_address
    ADD CONSTRAINT "FK_ua_id_user" FOREIGN KEY (id_user)
    REFERENCES public.user(id) ON UPDATE CASCADE ON DELETE RESTRICT;

ALTER TABLE ONLY public.user_address
    ADD CONSTRAINT "FK_ua_id_address" FOREIGN KEY (id_address)
    REFERENCES public.address(id) ON UPDATE CASCADE ON DELETE RESTRICT;


-- Create Stores Procedures --

CREATE OR REPLACE FUNCTION public.sp_trigger_user_before_update() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
	BEGIN
		IF NEW.dropped is TRUE
		THEN
           UPDATE public.user_address
           SET valid = FALSE
           WHERE user_address.id_user = NEW.id;
        END IF;

		RETURN NEW;
	END;
$$;

CREATE OR REPLACE FUNCTION public.sp_trigger_address_before_update() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
	BEGIN
		IF NEW.dropped is TRUE
		THEN
           UPDATE public.user_address
           SET valid = FALSE
           WHERE user_address.id_user = NEW.id;
        END IF;

		RETURN NEW;
	END;
$$;

CREATE OR REPLACE FUNCTION public.sp_trigger_user_address_before_insert() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
    DECLARE
        is_user_dropped boolean;
	    is_address_dropped boolean;
	BEGIN
	    SELECT u.dropped INTO is_user_dropped FROM public.user AS u WHERE u.id = NEW.id_user;
	    SELECT a.dropped INTO is_address_dropped FROM public.address AS a WHERE a.id = NEW.id_address;

	    -- raise notice 'Is user dropped?: %', is_user_dropped;
	    -- raise notice 'Is address dropped?: %', is_address_dropped;

		IF is_user_dropped is TRUE OR is_address_dropped is TRUE
		THEN
           NEW.valid := FALSE;
        END IF;

        -- raise notice 'Is valid?: %', NEW.valid;
		RETURN NEW;
	END;
$$;

-- Create Triggers --

DROP TRIGGER IF EXISTS tr_user_before_update ON public.user CASCADE;

CREATE TRIGGER tr_user_before_update
    BEFORE UPDATE ON public.user
    FOR EACH ROW
    EXECUTE FUNCTION public.sp_trigger_user_before_update();


DROP TRIGGER IF EXISTS tr_address_before_update ON public.user CASCADE;

CREATE TRIGGER tr_address_before_update
    BEFORE UPDATE ON public.address
    FOR EACH ROW
    EXECUTE FUNCTION public.sp_trigger_address_before_update();


DROP TRIGGER IF EXISTS tr_user_address_before_insert ON public.user_address CASCADE;

CREATE TRIGGER tr_user_address_before_insert
    BEFORE INSERT ON public.user_address
    FOR EACH ROW
    EXECUTE FUNCTION public.sp_trigger_user_address_before_insert();

-- Example Data --

INSERT INTO public.user(first_name, last_name, email, password, dropped) VALUES
    ('Juan', 'Perez', 'algo@mail.com', '12365478', false),
    ('Pedro', 'Sola', 'pedr@sola.com', 'asdfghjk', false),
    ('Lucas', 'Pato', 'lucas@pato.com', 'looney-T00NS', true);

INSERT INTO public.address(address_1, address_2, city, state, zip, country, dropped) VALUES
    ('Calle Odin', 'No. 45', 'CDMX', 'Ciudad de Mexico', '11985', 'Mexico', false),
    ('Calle Tlaloc', 'No. 108-A', 'CDMX', 'Ciudad de Mexico', '98574', 'Mexico', false),
    ('Calle San Pedro', 'B-40', 'CDMX', 'Ciudad de Mexico', '00985', 'Mexico', false),
    ('Calle Ulquiora', '00', 'Asuncion', 'Asuncion', '99999', 'Paraguay', true);

INSERT INTO public.user_address(id_user, id_address, valid) VALUES
    (1, 1, true),
    (1, 3, true),
    (2, 2, true),
    (3, 2, true),
    (2, 4, true),
    (3, 4, true);