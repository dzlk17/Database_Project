CREATE OR REPLACE FUNCTION topo.lista_droga_rejon()
RETURNS TABLE(id INT, droga VARCHAR, rejon VARCHAR) AS
$$
BEGIN
    RETURN QUERY
        SELECT d.id, d.nazwa, r.nazwa FROM topo.droga d
        JOIN topo.rejon r ON d.rejon_id = r.id
        ORDER BY r.nazwa;
END
$$
LANGUAGE 'plpgsql';

CREATE OR REPLACE FUNCTION topo.dodaj_przejscie(uzytkownik_id INT, droga_id INT)
RETURNS VOID AS
$$
BEGIN
    INSERT INTO topo.przejscia (id_uzytkownik, id_droga)
    VALUES (uzytkownik_id, droga_id);
END
$$
LANGUAGE 'plpgsql';

CREATE OR REPLACE FUNCTION topo.lista_przejsc(id_uz INT)
RETURNS TABLE(droga VARCHAR, rejon VARCHAR) AS
$$
BEGIN
    RETURN QUERY
        SELECT d.nazwa, r.nazwa FROM topo.przejscia p
        JOIN topo.droga d ON p.id_droga = d.id
        JOIN topo.rejon r ON d.rejon_id = r.id
        WHERE id_uz = p.id_uzytkownik;
END
$$
LANGUAGE 'plpgsql';

CREATE OR REPLACE FUNCTION topo.dodaj_droge(d_nazwa VARCHAR, d_wycena VARCHAR, rejon VARCHAR)
RETURNS VOID AS
$$
BEGIN
    INSERT INTO topo.droga (nazwa, wycena, rejon_id )
    SELECT d_nazwa, d_wycena, r.id FROM topo.rejon r
    WHERE r.nazwa = rejon;
END
$$
LANGUAGE 'plpgsql';

CREATE OR REPLACE FUNCTION topo.ranking()
RETURNS TABLE(miejsce BIGINT, login VARCHAR, imie VARCHAR, nazwisko VARCHAR, il BIGINT) AS
$$
BEGIN
    RETURN QUERY
        SELECT
	RANK () OVER (
		ORDER BY COUNT(p.id) DESC
	) miejsce, u.login, u.imie, u.nazwisko, COUNT(u.id) FROM topo.uzytkownik u
        JOIN topo.przejscia p ON u.id = p.id_uzytkownik
        GROUP BY u.id
        LIMIT 5;
    END
$$
LANGUAGE 'plpgsql';

CREATE OR REPLACE FUNCTION topo.droga_list(arg BIGINT)
RETURNS TABLE( miejsce BIGINT, droga VARCHAR, rejon VARCHAR, wycena BIGINT,il BIGINT) AS
$$
BEGIN
    RETURN QUERY
        SELECT RANK () OVER (
		ORDER BY
		    CASE WHEN arg = 1 THEN COUNT(p.id) END DESC,
            CASE WHEN arg = 2 THEN r.nazwa END,
            CASE WHEN arg = 3 THEN d.wycena END DESC
	    ) miejsce, d.nazwa, r.nazwa, d.wycena, COUNT(p.id) FROM topo.droga d
        JOIN topo.rejon r ON d.rejon_id = r.id
        JOIN topo.przejscia p ON d.id = p.id_droga
        GROUP BY d.id, r.id;
END
$$
LANGUAGE 'plpgsql';

CREATE OR REPLACE FUNCTION topo.area_list()
RETURNS TABLE( nazwa VARCHAR, opis VARCHAR, il BIGINT) AS
$$
BEGIN
    RETURN QUERY
        SELECT r.nazwa, r.opis, COUNT(d.id) FROM topo.rejon r
        JOIN topo.droga d ON d.rejon_id = r.id
        GROUP BY d.id, r.id
        ORDER BY count(d.id);
END
$$
LANGUAGE 'plpgsql';

CREATE OR REPLACE FUNCTION topo.walid_imie()
    RETURNS TRIGGER
    LANGUAGE plpgsql
    AS $$
    BEGIN
        IF NEW.imie LIKE '%[0-9]%' OR NEW.nazwisko LIKE '%[0-9]%' THEN
            RAISE EXCEPTION 'Cyfry w imieniu lub nazwisku';
        END IF;
        RETURN NULL;
    END
    $$;

CREATE TRIGGER walid_imie
BEFORE INSERT OR UPDATE ON topo.uzytkownik
FOR EACH ROW EXECUTE procedure topo.walid_imie();

CREATE OR REPLACE FUNCTION topo.zmien_klub(k_nazwa VARCHAR, u_id BIGINT)
    RETURNS VOID AS
$$
BEGIN
    UPDATE topo.uzytkownik
    SET id_klub =
            (SELECT id FROM topo.klub WHERE k_nazwa = topo.klub.nazwa)
    WHERE uzytkownik.id = u_id;
END
$$
    LANGUAGE 'plpgsql';
