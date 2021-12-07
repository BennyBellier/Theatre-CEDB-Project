-- TRIGGER gérant

CREATE TRIGGER date_Rep
BEFORE INSERT ON LesRepresentations
WHEN (SELECT COUNT(*)
        FROM LesRepresentations
        WHERE NEW.dateRep = dateRep) > 0
BEGIN
    SELECT RAISE(ABORT, 'Une representation utilise deja cette date');
END;\

CREATE TRIGGER PlaceOccupe
BEFORE INSERT ON LesTickets
WHEN (SELECT COUNT(*)
        FROM LesTickets
        WHERE NEW.dateRep = dateRep and ( NEW.noplace = noplace and NEW.norang = norang )) > 0
BEGIN
    SELECT RAISE(ABORT, 'Erreur : place déjà occupé !');
END;\