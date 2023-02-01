DROP SCHEMA topo CASCADE;
CREATE SCHEMA topo;

CREATE TABLE topo.uzytkownik(
    "id" SERIAL PRIMARY KEY,
    "login" VARCHAR(255) NOT NULL,
    "haslo" VARCHAR(255) NOT NULL,
    "nazwisko" VARCHAR(255) NOT NULL,
    "imie" VARCHAR(255) NOT NULL,
    "id_klub" INT,
    UNIQUE ("login")
);
CREATE TABLE topo.droga(
    "id" SERIAL PRIMARY KEY,
    "nazwa" VARCHAR(255) NOT NULL,
    "wycena" BIGINT NOT NULL,
    "rejon_id" BIGINT NOT NULL
);
CREATE TABLE topo.rejon(
    "id" SERIAL PRIMARY KEY,
    "nazwa" VARCHAR(255) NOT NULL,
    "opis" VARCHAR(255) NOT NULL,
    UNIQUE ("nazwa")

);
CREATE TABLE topo.przejscia(
    "id" SERIAL PRIMARY KEY,
    "id_uzytkownik" BIGINT NOT NULL,
    "id_droga" BIGINT NOT NULL
);
CREATE TABLE topo.przejscie_opis(
    "id" SERIAL PRIMARY KEY,
    "ocena" INT,
    "komentarz" VARCHAR(255),
    "styl" BIGINT NOT NULL,
    "data" DATE NOT NULL
);
CREATE TABLE topo.Klub(
    "id" SERIAL PRIMARY KEY,
    "nazwa" VARCHAR(255) NOT NULL,
    UNIQUE ("nazwa")

);

ALTER TABLE
    topo.przejscia ADD CONSTRAINT "przejscia_id_uzytkownik_foreign" FOREIGN KEY("id_uzytkownik") REFERENCES topo.uzytkownik("id") ON DELETE CASCADE;
ALTER TABLE
    topo.przejscia ADD CONSTRAINT "przejscia_id_droga_foreign" FOREIGN KEY("id_droga") REFERENCES topo.droga("id") ON DELETE CASCADE;
ALTER TABLE
    topo.droga ADD CONSTRAINT "droga_rejon_id_foreign" FOREIGN KEY("rejon_id") REFERENCES topo.rejon("id") ON DELETE CASCADE;
ALTER TABLE
    topo.uzytkownik ADD CONSTRAINT "uzytkownik_id_klub_foreign" FOREIGN KEY("id_klub") REFERENCES topo.Klub("id") ON DELETE SET NULL;
