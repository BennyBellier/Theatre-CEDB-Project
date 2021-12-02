-- Recuperation des valeur
insert into LesSpectacles(nomSpec, prixBaseSpec)
SELECT DISTINCT nomspec, prixbasespec FROM v0_LesRepresentations;

-- TODO 1.3 : Inventer des données dans les nouvelles tables (tout ce qui concerne les tickets). Par contre, utiliser une requête avec insert into qui transfère les données des tables de la V0 à celles de cette nouvelle version.
insert into LesSpectacles(nomSpec, prixBaseSpec) values ('Vérino', 9.50);
insert into LesSpectacles(nomSpec, prixBaseSpec) values ('Artus', 12.30);
insert into LesSpectacles(nomSpec, prixBaseSpec) values ('Guillaume Batz', 5);
insert into LesSpectacles(nomSpec, prixBaseSpec) values ('Paul Mirabel', 11);
insert into LesSpectacles(nomSpec, prixBaseSpec) values ('Laura Laune', 8.45);

-- insert into LesRepresentations(dateRep, promoRep, noSpec) values ('24/12/2019 17:00', 0.5, 1);
-- insert into LesRepresentations(dateRep, promoRep, noSpec) values ('24/12/2019 20:00', 0.3, 2);
-- insert into LesRepresentations(dateRep, promoRep, noSpec) values ('25/12/2019 20:00', 0, 4);
-- insert into LesRepresentations(dateRep, promoRep, noSpec) values ('21/12/2019 20:00', 0.2, 3);
-- insert into LesRepresentations(dateRep, promoRep, noSpec) values ('22/12/2019 20:00', 0.05, 5);
-- insert into LesRepresentations(dateRep, promoRep, noSpec) values ('05/01/2020 20:00', 0, 1);

-- Recuperation des valeurs de la BD V0
insert into LesRepresentations(dateRep, promoRep, noSpec)
WITH noSpecParNomSpec AS (SELECT nomspec, nospec FROM LesSpectacles)
SELECT daterep, (1-promorep), S.nospec
FROM V0_Lesrepresentations JOIN noSpecParNomSPec S USING (nomspec);

-- insert into LesZones (noZone, catZone) values (1, 'orchestre');
-- insert into LesZones (noZone, catZone) values (2, 'poulailler');
-- insert into LesZones (noZone, catZone) values (3, 'balcon');

-- Recuperation des valeurs de la BD V0
insert into LesZones(noZone, catZone)
SELECT DISTINCT nozone, catzone FROM V0_LESPLACES;

-- insert into TypeZones (catZone, tauxZone) values ('orchestre', 1.5);
-- insert into TypeZones (catZone, tauxZone) values ('balcon', 2);
-- insert into TypeZones (catZone, tauxZone) values ('poulailler', 1);

-- Recuperation des valeurs de la BD V0
insert into TypeZones(catZone, tauxZone)
SELECT DISTINCT catZone, tauxzone FROM V0_LESPLACES;

insert into LesReductions (typePers, tarifReduit) values ('ordinaire', 0);
insert into LesReductions (typePers, tarifReduit) values ('adhérent', 0.25);
insert into LesReductions (typePers, tarifReduit) values ('étudiant', 0.20);
insert into LesReductions (typePers, tarifReduit) values ('scolaire', 0.10);
insert into LesReductions (typePers, tarifReduit) values ('militaire', 0.05);
insert into LesReductions (typePers, tarifReduit) values ('sénior', 0.15);

insert into NumeroDossier (noDossier) values (1);
insert into NumeroDossier (noDossier) values (2);
insert into NumeroDossier (noDossier) values (3);
insert into NumeroDossier (noDossier) values (4);
insert into NumeroDossier (noDossier) values (5);
insert into NumeroDossier (noDossier) values (6);

insert into LesTickets (dateTrans, noPlace, noRang, typePers, noDossier, dateRep) values ('24/12/2019 16:45:15', 1, 1, 'adhérent', 1, '24/12/2019 17:00');
insert into LesTickets (dateTrans, noPlace, noRang, typePers, noDossier, dateRep) values ('24/12/2019 16:45:15', 2, 1, 'sénior', 1, '24/12/2019 17:00');
insert into LesTickets (dateTrans, noPlace, noRang, typePers, noDossier, dateRep) values ('24/12/2019 16:50:23', 1, 2, 'ordinaire', 2, '24/12/2019 17:00');
insert into LesTickets (dateTrans, noPlace, noRang, typePers, noDossier, dateRep) values ('24/12/2019 19:40:52', 1, 1, 'scolaire', 3, '24/12/2019 21:00');
insert into LesTickets (dateTrans, noPlace, noRang, typePers, noDossier, dateRep) values ('24/12/2019 19:40:52', 2, 1, 'scolaire', 3, '24/12/2019 21:00');
insert into LesTickets (dateTrans, noPlace, noRang, typePers, noDossier, dateRep) values ('24/12/2019 19:40:52', 1, 2, 'scolaire', 3, '24/12/2019 21:00');
insert into LesTickets (dateTrans, noPlace, noRang, typePers, noDossier, dateRep) values ('24/12/2019 19:40:52', 2, 2, 'scolaire', 3, '24/12/2019 21:00');
insert into LesTickets (dateTrans, noPlace, noRang, typePers, noDossier, dateRep) values ('24/12/2019 19:40:52', 3, 1, 'scolaire', 3, '24/12/2019 21:00');
insert into LesTickets (dateTrans, noPlace, noRang, typePers, noDossier, dateRep) values ('24/12/2019 19:40:52', 3, 2, 'scolaire', 3, '24/12/2019 21:00');
insert into LesTickets (dateTrans, noPlace, noRang, typePers, noDossier, dateRep) values ('24/12/2019 19:40:52', 4, 1, 'scolaire', 3, '24/12/2019 21:00');
insert into LesTickets (dateTrans, noPlace, noRang, typePers, noDossier, dateRep) values ('24/12/2019 19:40:52', 4, 2, 'scolaire', 3, '24/12/2019 21:00');
insert into LesTickets (dateTrans, noPlace, noRang, typePers, noDossier, dateRep) values ('24/12/2019 19:40:52', 5, 1, 'scolaire', 3, '24/12/2019 21:00');
insert into LesTickets (dateTrans, noPlace, noRang, typePers, noDossier, dateRep) values ('24/12/2019 19:40:52', 5, 2, 'scolaire', 3, '24/12/2019 21:00');
insert into LesTickets (dateTrans, noPlace, noRang, typePers, noDossier, dateRep) values ('24/12/2019 19:40:52', 1, 3, 'scolaire', 3, '24/12/2019 21:00');
insert into LesTickets (dateTrans, noPlace, noRang, typePers, noDossier, dateRep) values ('24/12/2019 19:40:52', 2, 3, 'scolaire', 3, '24/12/2019 21:00');
insert into LesTickets (dateTrans, noPlace, noRang, typePers, noDossier, dateRep) values ('24/12/2019 19:40:52', 3, 3, 'scolaire', 3, '24/12/2019 21:00');
insert into LesTickets (dateTrans, noPlace, noRang, typePers, noDossier, dateRep) values ('24/12/2019 19:40:52', 4, 3, 'scolaire', 3, '24/12/2019 21:00');
insert into LesTickets (dateTrans, noPlace, noRang, typePers, noDossier, dateRep) values ('24/12/2019 19:40:52', 5, 3, 'scolaire', 3, '24/12/2019 21:00');
insert into LesTickets (dateTrans, noPlace, noRang, typePers, noDossier, dateRep) values ('25/12/2019 19:55:10', 1, 2, 'militaire', 4, '25/12/2019 20:00');
insert into LesTickets (dateTrans, noPlace, noRang, typePers, noDossier, dateRep) values ('25/12/2019 19:55:10', 3, 3, 'ordinaire', 4, '25/12/2019 20:00');
insert into LesTickets (dateTrans, noPlace, noRang, typePers, noDossier, dateRep) values ('21/12/2019 19:45:36', 4, 4, 'sénior', 5, '26/12/2019 21:00');
insert into LesTickets (dateTrans, noPlace, noRang, typePers, noDossier, dateRep) values ('21/12/2019 19:45:36', 3, 1, 'sénior', 5, '26/12/2019 21:00');
insert into LesTickets (dateTrans, noPlace, noRang, typePers, noDossier, dateRep) values ('21/12/2019 19:57:24', 2, 1, 'étudiant', 6, '26/12/2019 21:00');
insert into LesTickets (dateTrans, noPlace, noRang, typePers, noDossier, dateRep) values ('21/12/2019 19:57:24', 5, 4, 'étudiant', 6, '26/12/2019 21:00');

-- Recuperation des valeurs de la BD V0
-- insert into LesVentes(


-- Recuperation des valeurs de la BD V0
INSERT INTO LesPlaces( noPlace, noRang, noZone)
SELECT noplace, norang, nozone FROM V0_LESPLACES;