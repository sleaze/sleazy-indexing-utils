
DROP TABLE IF EXISTS "User";
CREATE TABLE "User" (
    "id" integer,
    "name" varchar(64) NOT NULL UNIQUE,
    "deleted" boolean DEFAULT FALSE,
    "createdTs" timestamp DEFAULT current_timestamp,
    "modifiedTs" timestamp DEFAULT NULL,
    PRIMARY KEY (id)
);

DROP TABLE IF EXISTS "Video";
CREATE TABLE "Video" (
    "id" integer,
    "userId" integer,
    "title" varchar(60) DEFAULT NULL,
    "description" text DEFAULT NULL,
    "duration" interval DEFAULT NULL,
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
    "title" varchar(60) DEFAULT NULL,
    "description" text DEFAULT NULL,
    "imageIds" integer[],
    "deleted" boolean DEFAULT FALSE,
    "createdTs" timestamp DEFAULT current_timestamp,
    "modifiedTs" timestamp DEFAULT NULL,
    FOREIGN KEY ("userId") REFERENCES "User" ("id") DEFERRABLE INITIALLY DEFERRED,
    PRIMARY KEY (id)
);


