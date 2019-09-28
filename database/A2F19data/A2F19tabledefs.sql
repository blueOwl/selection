CREATE TABLE responsible_parties
(
    id integer NOT NULL,
    nct_id character varying,
    responsible_party_type character varying,
    name character varying ,
    title character varying ,
    organization character varying ,
    affiliation text,
    CONSTRAINT responsible_parties_pkey PRIMARY KEY (id)
);

CREATE TABLE sponsors
(
    id integer NOT NULL,
    nct_id character varying,
    agency_class character varying,
    lead_or_collaborator character varying,
    name character varying,
    CONSTRAINT sponsors_pkey PRIMARY KEY (id)
);

CREATE TABLE overall_officials
(
    id integer NOT NULL,
    nct_id character varying,
    role character varying,
    name character varying,
    affiliation character varying,
    CONSTRAINT overall_officials_pkey PRIMARY KEY (id)
);


CREATE TABLE factor (
    category varchar(200),
    condition varchar(200),
    CONSTRAINT factor_pk PRIMARY KEY(category, condition)
);

CREATE TABLE studies (
    nct_id CHARACTER(11),
    start_date DATE,
    start_date_type CHARACTER(11),
    completion_date DATE,
    completion_date_type CHARACTER(11),
    study_type  VARCHAR(35),
    brief_title VARCHAR(350),
    overall_status   VARCHAR(35),
    phase   VARCHAR(20),
    enrollment INTEGER,
    enrollment_type CHARACTER(11),
    source VARCHAR(150),
    why_stopped VARCHAR(200),
    is_fda_regulated_drug BOOLEAN,
    CONSTRAINT studies_pk PRIMARY KEY(nct_id)
);


CREATE TABLE conditions (
    id INTEGER,
    nct_id CHARACTER(11),
    name VARCHAR(200),
    downcase_name VARCHAR(200),
    CONSTRAINT conditions_pk PRIMARY KEY(id)
);
CREATE INDEX conditions_nct_id on conditions(nct_id);
CREATE INDEX conditions_name on conditions(name);
