CREATE TABLE umwelt_panels (
    table_name character varying(255) NOT NULL,
    core_kpi character varying(255) NOT NULL ,
    measurement character varying(255) NOT NULL,
    land character varying (255) NOT NULL ,
    year INT NOT NULL , 
    value FLOAT NOT NULL  
);