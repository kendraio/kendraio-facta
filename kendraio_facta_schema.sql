--
-- PostgreSQL database dump
--

-- Dumped from database version 9.6.7
-- Dumped by pg_dump version 9.6.7

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: received_statements; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE received_statements (
    id bigint NOT NULL,
    "time" timestamp with time zone,
    subject character varying,
    server_program_id character varying,
    semantic_store_id character varying,
    statement json,
    sha256_hash character varying
);


ALTER TABLE received_statements OWNER TO postgres;

--
-- Name: received_statements_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE received_statements_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE received_statements_id_seq OWNER TO postgres;

--
-- Name: received_statements_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE received_statements_id_seq OWNED BY received_statements.id;


--
-- Name: received_statements id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY received_statements ALTER COLUMN id SET DEFAULT nextval('received_statements_id_seq'::regclass);


--
-- Name: received_statements received_statements_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY received_statements
    ADD CONSTRAINT received_statements_pkey PRIMARY KEY (id);


--
-- Name: TABLE received_statements; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE received_statements TO kendraio_facta;


--
-- Name: SEQUENCE received_statements_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE received_statements_id_seq TO kendraio_facta;


--
-- PostgreSQL database dump complete
--

