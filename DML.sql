INSERT INTO topo.klub (nazwa) VALUES
    ('Climb Zone'),
    ('Klub sportowy kraków');

INSERT INTO topo.uzytkownik (login, nazwisko, imie, haslo) VALUES
    ('ADMIN', 'ADMIN', 'ADMIN', 'ADMIN');

INSERT INTO topo.uzytkownik (login, nazwisko, imie, haslo, id_klub) VALUES
    ('dzlk', 'Kowalsi', 'Jan', '1234', 1),
    ('mlk', 'Nowak', 'Jacek', 'jck', 1);

INSERT INTO topo.rejon (nazwa, opis) VALUES
    ('Góra kołoczek', 'Duzy rejon niedaleko Olsztyna'),
    ('Boniek', 'Duża grupa skalna w rezerwacie Sokole Góry');

INSERT INTO topo.droga (nazwa, wycena, rejon_id) VALUES
    ('Lekcja Tańca', 5, 1),
    ('Wejście smoka', 6, 2);

INSERT INTO topo.przejscia(id_uzytkownik, id_droga) VALUES
    (2, 1),
    (2, 2),
    (2, 1),
    (3, 1),
    (3, 2),
    (3, 1);

