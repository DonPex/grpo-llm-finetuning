--
-- PostgreSQL database dump
--

-- Dumped from database version 17.0 (Debian 17.0-1.pgdg120+1)
-- Dumped by pg_dump version 17.4 (Ubuntu 17.4-1.pgdg22.04+2)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: tmf724_incident_management; Type: SCHEMA; Schema: -; Owner: mitobi
--

CREATE SCHEMA tmf724_incident_management;


ALTER SCHEMA tmf724_incident_management OWNER TO mitobi;

--
-- Name: impact_type; Type: TYPE; Schema: tmf724_incident_management; Owner: mitobi
--

CREATE TYPE tmf724_incident_management.impact_type AS ENUM (
    'extensive',
    'significant',
    'moderate',
    'minor'
);


ALTER TYPE tmf724_incident_management.impact_type OWNER TO mitobi;

--
-- Name: incident_ack_state_type; Type: TYPE; Schema: tmf724_incident_management; Owner: mitobi
--

CREATE TYPE tmf724_incident_management.incident_ack_state_type AS ENUM (
    'acknowledged',
    'unacknowledged'
);


ALTER TYPE tmf724_incident_management.incident_ack_state_type OWNER TO mitobi;

--
-- Name: incident_state_type; Type: TYPE; Schema: tmf724_incident_management; Owner: mitobi
--

CREATE TYPE tmf724_incident_management.incident_state_type AS ENUM (
    'raised',
    'updated',
    'cleared'
);


ALTER TYPE tmf724_incident_management.incident_state_type OWNER TO mitobi;

--
-- Name: priority_type; Type: TYPE; Schema: tmf724_incident_management; Owner: mitobi
--

CREATE TYPE tmf724_incident_management.priority_type AS ENUM (
    'critical',
    'high',
    'medium',
    'low'
);


ALTER TYPE tmf724_incident_management.priority_type OWNER TO mitobi;

--
-- Name: urgency_type; Type: TYPE; Schema: tmf724_incident_management; Owner: mitobi
--

CREATE TYPE tmf724_incident_management.urgency_type AS ENUM (
    'critical',
    'high',
    'medium',
    'low'
);


ALTER TYPE tmf724_incident_management.urgency_type OWNER TO mitobi;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: characteristic; Type: TABLE; Schema: tmf724_incident_management; Owner: mitobi
--

CREATE TABLE tmf724_incident_management.characteristic (
    id integer NOT NULL,
    name character varying(50),
    value character varying(50),
    value_type character varying(50),
    incident_id integer
);


ALTER TABLE tmf724_incident_management.characteristic OWNER TO mitobi;

--
-- Name: characteristic_id_seq; Type: SEQUENCE; Schema: tmf724_incident_management; Owner: mitobi
--

CREATE SEQUENCE tmf724_incident_management.characteristic_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE tmf724_incident_management.characteristic_id_seq OWNER TO mitobi;

--
-- Name: characteristic_id_seq; Type: SEQUENCE OWNED BY; Schema: tmf724_incident_management; Owner: mitobi
--

ALTER SEQUENCE tmf724_incident_management.characteristic_id_seq OWNED BY tmf724_incident_management.characteristic.id;


--
-- Name: characteristic_relationship; Type: TABLE; Schema: tmf724_incident_management; Owner: mitobi
--

CREATE TABLE tmf724_incident_management.characteristic_relationship (
    id integer NOT NULL,
    href character varying(255),
    relationship_type character varying(50),
    characteristic_id integer
);


ALTER TABLE tmf724_incident_management.characteristic_relationship OWNER TO mitobi;

--
-- Name: characteristic_relationship_id_seq; Type: SEQUENCE; Schema: tmf724_incident_management; Owner: mitobi
--

CREATE SEQUENCE tmf724_incident_management.characteristic_relationship_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE tmf724_incident_management.characteristic_relationship_id_seq OWNER TO mitobi;

--
-- Name: characteristic_relationship_id_seq; Type: SEQUENCE OWNED BY; Schema: tmf724_incident_management; Owner: mitobi
--

ALTER SEQUENCE tmf724_incident_management.characteristic_relationship_id_seq OWNED BY tmf724_incident_management.characteristic_relationship.id;


--
-- Name: entity_ref; Type: TABLE; Schema: tmf724_incident_management; Owner: mitobi
--

CREATE TABLE tmf724_incident_management.entity_ref (
    id integer NOT NULL,
    href character varying(255),
    name character varying(50),
    ref_id integer,
    incident_id integer
);


ALTER TABLE tmf724_incident_management.entity_ref OWNER TO mitobi;

--
-- Name: entity_ref_id_seq; Type: SEQUENCE; Schema: tmf724_incident_management; Owner: mitobi
--

CREATE SEQUENCE tmf724_incident_management.entity_ref_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE tmf724_incident_management.entity_ref_id_seq OWNER TO mitobi;

--
-- Name: entity_ref_id_seq; Type: SEQUENCE OWNED BY; Schema: tmf724_incident_management; Owner: mitobi
--

ALTER SEQUENCE tmf724_incident_management.entity_ref_id_seq OWNED BY tmf724_incident_management.entity_ref.id;


--
-- Name: external_identifier; Type: TABLE; Schema: tmf724_incident_management; Owner: mitobi
--

CREATE TABLE tmf724_incident_management.external_identifier (
    external_identifier_id integer NOT NULL,
    external_identifier_type character varying(50),
    href character varying(255),
    id character varying(50),
    owner character varying(50),
    incident_id integer
);


ALTER TABLE tmf724_incident_management.external_identifier OWNER TO mitobi;

--
-- Name: external_identifier_external_identifier_id_seq; Type: SEQUENCE; Schema: tmf724_incident_management; Owner: mitobi
--

CREATE SEQUENCE tmf724_incident_management.external_identifier_external_identifier_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE tmf724_incident_management.external_identifier_external_identifier_id_seq OWNER TO mitobi;

--
-- Name: external_identifier_external_identifier_id_seq; Type: SEQUENCE OWNED BY; Schema: tmf724_incident_management; Owner: mitobi
--

ALTER SEQUENCE tmf724_incident_management.external_identifier_external_identifier_id_seq OWNED BY tmf724_incident_management.external_identifier.external_identifier_id;


--
-- Name: incident; Type: TABLE; Schema: tmf724_incident_management; Owner: mitobi
--

CREATE TABLE tmf724_incident_management.incident (
    id integer NOT NULL,
    ack_state tmf724_incident_management.incident_ack_state_type,
    ack_time timestamp with time zone,
    category character varying(50),
    clear_time timestamp with time zone,
    domain character varying(50),
    href character varying(255),
    impact tmf724_incident_management.impact_type,
    detail text,
    resolution_suggestion text,
    name character varying(255),
    occur_time timestamp with time zone,
    priority tmf724_incident_management.priority_type,
    state tmf724_incident_management.incident_state_type,
    update_time timestamp with time zone,
    urgency tmf724_incident_management.urgency_type
);


ALTER TABLE tmf724_incident_management.incident OWNER TO mitobi;

--
-- Name: incident_id_seq; Type: SEQUENCE; Schema: tmf724_incident_management; Owner: mitobi
--

CREATE SEQUENCE tmf724_incident_management.incident_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE tmf724_incident_management.incident_id_seq OWNER TO mitobi;

--
-- Name: incident_id_seq; Type: SEQUENCE OWNED BY; Schema: tmf724_incident_management; Owner: mitobi
--

ALTER SEQUENCE tmf724_incident_management.incident_id_seq OWNED BY tmf724_incident_management.incident.id;


--
-- Name: resource_entity; Type: TABLE; Schema: tmf724_incident_management; Owner: mitobi
--

CREATE TABLE tmf724_incident_management.resource_entity (
    resource_entity_id integer NOT NULL,
    href character varying(255),
    object_id character varying(50),
    object_type character varying(50),
    incident_id integer
);


ALTER TABLE tmf724_incident_management.resource_entity OWNER TO mitobi;

--
-- Name: resource_entity_resource_entity_id_seq; Type: SEQUENCE; Schema: tmf724_incident_management; Owner: mitobi
--

CREATE SEQUENCE tmf724_incident_management.resource_entity_resource_entity_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE tmf724_incident_management.resource_entity_resource_entity_id_seq OWNER TO mitobi;

--
-- Name: resource_entity_resource_entity_id_seq; Type: SEQUENCE OWNED BY; Schema: tmf724_incident_management; Owner: mitobi
--

ALTER SEQUENCE tmf724_incident_management.resource_entity_resource_entity_id_seq OWNED BY tmf724_incident_management.resource_entity.resource_entity_id;


--
-- Name: root_cause; Type: TABLE; Schema: tmf724_incident_management; Owner: mitobi
--

CREATE TABLE tmf724_incident_management.root_cause (
    root_cause_id integer NOT NULL,
    href character varying(255),
    object_id character varying(50),
    object_type character varying(50),
    location character varying(50),
    name character varying(50),
    incident_id integer
);


ALTER TABLE tmf724_incident_management.root_cause OWNER TO mitobi;

--
-- Name: root_cause_root_cause_id_seq; Type: SEQUENCE; Schema: tmf724_incident_management; Owner: mitobi
--

CREATE SEQUENCE tmf724_incident_management.root_cause_root_cause_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE tmf724_incident_management.root_cause_root_cause_id_seq OWNER TO mitobi;

--
-- Name: root_cause_root_cause_id_seq; Type: SEQUENCE OWNED BY; Schema: tmf724_incident_management; Owner: mitobi
--

ALTER SEQUENCE tmf724_incident_management.root_cause_root_cause_id_seq OWNED BY tmf724_incident_management.root_cause.root_cause_id;


--
-- Name: characteristic id; Type: DEFAULT; Schema: tmf724_incident_management; Owner: mitobi
--

ALTER TABLE ONLY tmf724_incident_management.characteristic ALTER COLUMN id SET DEFAULT nextval('tmf724_incident_management.characteristic_id_seq'::regclass);


--
-- Name: characteristic_relationship id; Type: DEFAULT; Schema: tmf724_incident_management; Owner: mitobi
--

ALTER TABLE ONLY tmf724_incident_management.characteristic_relationship ALTER COLUMN id SET DEFAULT nextval('tmf724_incident_management.characteristic_relationship_id_seq'::regclass);


--
-- Name: entity_ref id; Type: DEFAULT; Schema: tmf724_incident_management; Owner: mitobi
--

ALTER TABLE ONLY tmf724_incident_management.entity_ref ALTER COLUMN id SET DEFAULT nextval('tmf724_incident_management.entity_ref_id_seq'::regclass);


--
-- Name: external_identifier external_identifier_id; Type: DEFAULT; Schema: tmf724_incident_management; Owner: mitobi
--

ALTER TABLE ONLY tmf724_incident_management.external_identifier ALTER COLUMN external_identifier_id SET DEFAULT nextval('tmf724_incident_management.external_identifier_external_identifier_id_seq'::regclass);


--
-- Name: incident id; Type: DEFAULT; Schema: tmf724_incident_management; Owner: mitobi
--

ALTER TABLE ONLY tmf724_incident_management.incident ALTER COLUMN id SET DEFAULT nextval('tmf724_incident_management.incident_id_seq'::regclass);


--
-- Name: resource_entity resource_entity_id; Type: DEFAULT; Schema: tmf724_incident_management; Owner: mitobi
--

ALTER TABLE ONLY tmf724_incident_management.resource_entity ALTER COLUMN resource_entity_id SET DEFAULT nextval('tmf724_incident_management.resource_entity_resource_entity_id_seq'::regclass);


--
-- Name: root_cause root_cause_id; Type: DEFAULT; Schema: tmf724_incident_management; Owner: mitobi
--

ALTER TABLE ONLY tmf724_incident_management.root_cause ALTER COLUMN root_cause_id SET DEFAULT nextval('tmf724_incident_management.root_cause_root_cause_id_seq'::regclass);


--
-- Name: characteristic characteristic_pkey; Type: CONSTRAINT; Schema: tmf724_incident_management; Owner: mitobi
--

ALTER TABLE ONLY tmf724_incident_management.characteristic
    ADD CONSTRAINT characteristic_pkey PRIMARY KEY (id);


--
-- Name: characteristic_relationship characteristic_relationship_pkey; Type: CONSTRAINT; Schema: tmf724_incident_management; Owner: mitobi
--

ALTER TABLE ONLY tmf724_incident_management.characteristic_relationship
    ADD CONSTRAINT characteristic_relationship_pkey PRIMARY KEY (id);


--
-- Name: entity_ref entity_ref_pkey; Type: CONSTRAINT; Schema: tmf724_incident_management; Owner: mitobi
--

ALTER TABLE ONLY tmf724_incident_management.entity_ref
    ADD CONSTRAINT entity_ref_pkey PRIMARY KEY (id);


--
-- Name: external_identifier external_identifier_pkey; Type: CONSTRAINT; Schema: tmf724_incident_management; Owner: mitobi
--

ALTER TABLE ONLY tmf724_incident_management.external_identifier
    ADD CONSTRAINT external_identifier_pkey PRIMARY KEY (external_identifier_id);


--
-- Name: incident incident_pkey; Type: CONSTRAINT; Schema: tmf724_incident_management; Owner: mitobi
--

ALTER TABLE ONLY tmf724_incident_management.incident
    ADD CONSTRAINT incident_pkey PRIMARY KEY (id);


--
-- Name: resource_entity resource_entity_pkey; Type: CONSTRAINT; Schema: tmf724_incident_management; Owner: mitobi
--

ALTER TABLE ONLY tmf724_incident_management.resource_entity
    ADD CONSTRAINT resource_entity_pkey PRIMARY KEY (resource_entity_id);


--
-- Name: root_cause root_cause_pkey; Type: CONSTRAINT; Schema: tmf724_incident_management; Owner: mitobi
--

ALTER TABLE ONLY tmf724_incident_management.root_cause
    ADD CONSTRAINT root_cause_pkey PRIMARY KEY (root_cause_id);


--
-- Name: characteristic characteristic_incident_id_fkey; Type: FK CONSTRAINT; Schema: tmf724_incident_management; Owner: mitobi
--

ALTER TABLE ONLY tmf724_incident_management.characteristic
    ADD CONSTRAINT characteristic_incident_id_fkey FOREIGN KEY (incident_id) REFERENCES tmf724_incident_management.incident(id);


--
-- Name: characteristic_relationship characteristic_relationship_characteristic_id_fkey; Type: FK CONSTRAINT; Schema: tmf724_incident_management; Owner: mitobi
--

ALTER TABLE ONLY tmf724_incident_management.characteristic_relationship
    ADD CONSTRAINT characteristic_relationship_characteristic_id_fkey FOREIGN KEY (characteristic_id) REFERENCES tmf724_incident_management.characteristic(id);


--
-- Name: entity_ref entity_ref_incident_id_fkey; Type: FK CONSTRAINT; Schema: tmf724_incident_management; Owner: mitobi
--

ALTER TABLE ONLY tmf724_incident_management.entity_ref
    ADD CONSTRAINT entity_ref_incident_id_fkey FOREIGN KEY (incident_id) REFERENCES tmf724_incident_management.incident(id);


--
-- Name: external_identifier external_identifier_incident_id_fkey; Type: FK CONSTRAINT; Schema: tmf724_incident_management; Owner: mitobi
--

ALTER TABLE ONLY tmf724_incident_management.external_identifier
    ADD CONSTRAINT external_identifier_incident_id_fkey FOREIGN KEY (incident_id) REFERENCES tmf724_incident_management.incident(id);


--
-- Name: resource_entity resource_entity_incident_id_fkey; Type: FK CONSTRAINT; Schema: tmf724_incident_management; Owner: mitobi
--

ALTER TABLE ONLY tmf724_incident_management.resource_entity
    ADD CONSTRAINT resource_entity_incident_id_fkey FOREIGN KEY (incident_id) REFERENCES tmf724_incident_management.incident(id);


--
-- Name: root_cause root_cause_incident_id_fkey; Type: FK CONSTRAINT; Schema: tmf724_incident_management; Owner: mitobi
--

ALTER TABLE ONLY tmf724_incident_management.root_cause
    ADD CONSTRAINT root_cause_incident_id_fkey FOREIGN KEY (incident_id) REFERENCES tmf724_incident_management.incident(id);


--
-- PostgreSQL database dump complete
--

