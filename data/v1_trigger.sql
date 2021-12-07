-- TRIGGER gérant

CREATE TRIGGER date_Rep
BEFORE INSERT ON LesRepresentations
WHEN (SELECT COUNT(*)
        FROM LesRepresentations
        WHERE NEW.dateRep = dateRep) > 0
BEGIN
    SELECT RAISE(ABORT, 'Une representation utilise deja cette date');
END;\