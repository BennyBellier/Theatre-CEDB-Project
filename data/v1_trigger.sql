-- TRIGGER gérant

CREATE TRIGGER trig_same_date
BEFORE INSERT ON LesRepresentations
WHEN (SELECT COUNT(*)
        FROM LesRepresentations
        WHERE NEW.dateRep = dateRep) > 0
BEGIN
    SELECT RAISE(ABORT, 'Une representation utilise deja cette date');
END;\

CREATE TRIGGER trig_RepresentationObsolete
BEFORE INSERT ON lesRepresentations
WHEN (SELECT COUNT(*)
        FROM LesRepresentations
        WHERE NEW.dateRep <= DATE()) > 0
BEGIN
    SELECT RAISE(ABORT, 'Erreur : la date spécifié est est déjà passé');
END;\

CREATE TRIGGER trig_PlaceOccupe
BEFORE INSERT ON LesTickets
WHEN (SELECT COUNT(*)
        FROM LesTickets
        WHERE NEW.dateRep = dateRep and ( NEW.noplace = noplace and NEW.norang = norang )) > 0
BEGIN
    SELECT RAISE(ABORT, 'Erreur : place déjà occupé !');
END;\

CREATE TRIGGER trig_TicketLate
BEFORE INSERT ON lesTickets
WHEN (SELECT COUNT(*)
        FROM LesTickets
        WHERE NEW.dateTrans > dateRep) > 0
BEGIN
    SELECT RAISE(ABORT, 'Erreur : la date spécifié est est déjà passé');
END;\