CREATE TABLE public.ais
(
    "MMSI" integer NOT NULL,
    "BaseDateTime" timestamp without time zone,
    "LAT" double precision,
    "LON" double precision,
    "SOG" double precision,
    "COG" double precision,
    "Heading" double precision,
    "VesselName" text,
    "IMO" text,
    "CallSign" text,
    "VesselType" double precision,
    "Status" text,
    "Length" double precision,
    "Width" double precision,
    "Draft" double precision,
    "Cargo" double precision,
    "Zone" integer,
)
WITH (
    OIDS = FALSE
);

ALTER TABLE public.ais
    OWNER to mydbinstance;