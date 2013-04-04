
BEGIN;

SET CONSTRAINTS ALL DEFERRED;

DROP SEQUENCE IF EXISTS "User_id_seq";
CREATE SEQUENCE "User_id_seq" START 1;

DROP TABLE IF EXISTS "User" CASCADE;
CREATE TABLE "User" (
    "id" integer PRIMARY KEY DEFAULT nextval('"User_id_seq"'),
    "name" varchar(128) NOT NULL UNIQUE,
    "deleted" boolean DEFAULT FALSE,
    "createdTs" timestamp DEFAULT current_timestamp,
    "modifiedTs" timestamp DEFAULT NULL
);

DROP TABLE IF EXISTS "Video";
CREATE TABLE "Video" (
    "id" integer,
    "userId" integer,
    "title" varchar(256) DEFAULT NULL,
    "description" text DEFAULT NULL,
    "duration" interval DEFAULT NULL,
    "categories" varchar(128)[] DEFAULT NULL,
    "deleted" boolean DEFAULT FALSE,
    "createdTs" timestamp DEFAULT current_timestamp,
    "modifiedTs" timestamp DEFAULT NULL,
    FOREIGN KEY ("userId") REFERENCES "User" ("id") DEFERRABLE INITIALLY DEFERRED,
    PRIMARY KEY (id)
);

DROP TABLE IF EXISTS "Gallery";
CREATE TABLE "Gallery" (
    "id" integer,
    "userId" integer,
    "title" varchar(256) DEFAULT NULL,
    "description" text DEFAULT NULL,
    "imageIds" integer[],
    "categories" varchar(128)[] DEFAULT NULL,
    "deleted" boolean DEFAULT FALSE,
    "createdTs" timestamp DEFAULT current_timestamp,
    "modifiedTs" timestamp DEFAULT NULL,
    FOREIGN KEY ("userId") REFERENCES "User" ("id") DEFERRABLE INITIALLY DEFERRED,
    PRIMARY KEY (id)
);

COMMIT;

