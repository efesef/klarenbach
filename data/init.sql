CREATE TABLE movies (
    movie_id character varying(255) NOT NULL unique,
    movie_name character varying(255) NOT NULL ,
    release_dates timestamp without time zone NOT NULL,
    reviews float 
);

INSERT INTO movies (movie_id, movie_name, release_dates, reviews)
VALUES ('fjaads', 'dummy', '1990-01-01 00:00:00', 5);