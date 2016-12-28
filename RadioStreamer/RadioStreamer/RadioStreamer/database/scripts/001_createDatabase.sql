CREATE TABLE public.channel
(
    id serial,
    name text COLLATE pg_catalog."default" NOT NULL,
    page_url text COLLATE pg_catalog."default" NOT NULL,
    stream_url text COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT channel_pkey PRIMARY KEY (id)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.channel
    OWNER to postgres;
	
---------------------------------------------------------------------

CREATE TABLE public.person
(
	user_id serial,
    CONSTRAINT person_pkey PRIMARY KEY (user_id),
    FOREIGN KEY (user_id)
        REFERENCES public.auth_user (id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.person
    OWNER to postgres;
	
---------------------------------------------------------------------

CREATE TABLE public.tag
(
	id serial,
    name text COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT tag_pkey PRIMARY KEY (id),
    CONSTRAINT tag_name_key UNIQUE (name)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.tag
    OWNER to postgres;
	
---------------------------------------------------------------------

CREATE TABLE public.favourites
(
    id bigserial,
    channel_id integer NOT NULL,
    person_id bigint NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (channel_id)
        REFERENCES public.channel (id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    FOREIGN KEY (person_id)
        REFERENCES public.person (id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.favourites
    OWNER to postgres;
	
---------------------------------------------------------------------

CREATE TABLE public.history
(
	id bigserial,
    channel_id integer NOT NULL,
    person_id bigint NOT NULL,
    start_date timestamp without time zone NOT NULL,
    end_date timestamp without time zone NOT NULL,
    duration integer NOT NULL,
	PRIMARY KEY(id),
    CONSTRAINT history_channel_id_fkey FOREIGN KEY (channel_id)
        REFERENCES public.channel (id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT history_person_id_fkey FOREIGN KEY (person_id)
        REFERENCES public.person (id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.history
    OWNER to postgres;
	
---------------------------------------------------------------------

CREATE TABLE public.ratings
(
    id bigserial,
    channel_id integer NOT NULL,
    person_id bigint NOT NULL,
    value smallint NOT NULL,
    PRIMARY KEY (id),
    CONSTRAINT ratings_channel_id_fkey FOREIGN KEY (channel_id)
        REFERENCES public.channel (id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT ratings_person_id_fkey FOREIGN KEY (person_id)
        REFERENCES public.person (id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT ratings_value_check CHECK (value >= 1 AND value <= 10)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.ratings
    OWNER to postgres;
	
---------------------------------------------------------------------

CREATE TABLE public.tags_channels
(
	id serial,
    channel_id integer NOT NULL,
    tag_id integer NOT NULL,
	PRIMARY KEY(id),
    CONSTRAINT tags_channels_channel_id_fkey FOREIGN KEY (channel_id)
        REFERENCES public.channel (id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT tags_channels_tag_id_fkey FOREIGN KEY (tag_id)
        REFERENCES public.tag (id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.tags_channels
    OWNER to postgres;