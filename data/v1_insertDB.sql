-- Recuperation des valeur
INSERT INTO LesSpectacles(nomSpec, prixBaseSpec)
SELECT DISTINCT nomspec, prixbasespec FROM v0_LesRepresentations;

-- TODO 1.3 : Inventer des données dans les nouvelles tables (tout ce qui concerne les tickets). Par contre, utiliser une requête avec INSERT INTO qui transfère les données des tables de la V0 à celles de cette nouvelle version.
INSERT INTO LesSpectacles(nomSpec, prixBaseSpec)
VALUES
  ('Vérino', 9.50),
  ('Artus', 12.30),
  ('Guillaume Batz', 5),
  ('Paul Mirabel', 11),
  ('Laura Laune', 8.45);

-- Recuperation des valeurs de la BD V0
INSERT INTO LesRepresentations(dateRep, promoRep, noSpec)
WITH noSpecParNomSpec AS (SELECT nomspec, nospec FROM LesSpectacles)
SELECT daterep, (1-promorep), S.nospec
FROM V0_Lesrepresentations JOIN noSpecParNomSPec S USING (nomspec);

-- Recuperation des valeurs de la BD V0
INSERT INTO TypeZones(catZone, tauxZone)
SELECT DISTINCT catZone, tauxzone FROM V0_LESPLACES;

-- Recuperation des valeurs de la BD V0
INSERT INTO LesZones(noZone, catZone)
SELECT DISTINCT nozone, catzone FROM V0_LESPLACES;

-- Recuperation des valeurs de la BD V0
INSERT INTO LesPlaces( noPlace, noRang, noZone)
SELECT noplace, norang, nozone FROM V0_LESPLACES;

INSERT INTO LesReductions (typePers, tarifReduit)
VALUES
  ('ordinaire', 0),
  ('adhérent', 0.25),
  ('étudiant', 0.20),
  ('scolaire', 0.10),
  ('militaire', 0.05),
  ('sénior', 0.15);

INSERT INTO NumeroDossier (noDossier)
VALUES
  (1),
  (2),
  (3),
  (4),
  (5),
  (6);

INSERT INTO LesTickets (dateTrans, noPlace, noRang, typePers, noDossier, dateRep)
VALUES
  ('24/12/2019 16:45:15', 1, 1, 'adhérent', 1, '24/12/2019 17:00'),
  ('24/12/2019 16:45:15', 2, 1, 'sénior', 1, '24/12/2019 17:00'),
  ('24/12/2019 16:50:23', 1, 2, 'ordinaire', 2, '24/12/2019 17:00'),
  ('24/12/2019 19:40:52', 1, 1, 'scolaire', 3, '24/12/2019 21:00'),
  ('24/12/2019 19:40:52', 2, 1, 'scolaire', 3, '24/12/2019 21:00'),
  ('24/12/2019 19:40:52', 1, 2, 'scolaire', 3, '24/12/2019 21:00'),
  ('24/12/2019 19:40:52', 2, 2, 'scolaire', 3, '24/12/2019 21:00'),
  ('24/12/2019 19:40:52', 3, 1, 'scolaire', 3, '24/12/2019 21:00'),
  ('24/12/2019 19:40:52', 3, 2, 'scolaire', 3, '24/12/2019 21:00'),
  ('24/12/2019 19:40:52', 4, 1, 'scolaire', 3, '24/12/2019 21:00'),
  ('24/12/2019 19:40:52', 4, 2, 'scolaire', 3, '24/12/2019 21:00'),
  ('24/12/2019 19:40:52', 5, 1, 'scolaire', 3, '24/12/2019 21:00'),
  ('24/12/2019 19:40:52', 5, 2, 'scolaire', 3, '24/12/2019 21:00'),
  ('24/12/2019 19:40:52', 1, 3, 'scolaire', 3, '24/12/2019 21:00'),
  ('24/12/2019 19:40:52', 2, 3, 'scolaire', 3, '24/12/2019 21:00'),
  ('24/12/2019 19:40:52', 3, 3, 'scolaire', 3, '24/12/2019 21:00'),
  ('24/12/2019 19:40:52', 4, 3, 'scolaire', 3, '24/12/2019 21:00'),
  ('24/12/2019 19:40:52', 5, 3, 'scolaire', 3, '24/12/2019 21:00'),
  ('25/12/2019 19:55:10', 1, 2, 'militaire', 4, '25/12/2019 20:00'),
  ('25/12/2019 19:55:10', 3, 3, 'ordinaire', 4, '25/12/2019 20:00'),
  ('21/12/2019 19:45:36', 4, 4, 'sénior', 5, '26/12/2019 21:00'),
  ('21/12/2019 19:45:36', 3, 1, 'sénior', 5, '26/12/2019 21:00'),
  ('21/12/2019 19:57:24', 2, 1, 'étudiant', 6, '26/12/2019 21:00'),
  ('21/12/2019 19:57:24', 5, 4, 'étudiant', 6, '26/12/2019 21:00');