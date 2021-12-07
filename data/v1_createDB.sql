-- Activation des foreigns keys

PRAGMA foreign_keys = ON;

-- FAIS 1.3 : Créer les tables manquantes et modifier celles ci-dessous

create table LesSpectacles (
    noSpec integer primary key,
    nomSpec varchar(50) not null unique,
    prixBaseSpec decimal (6,2) not null,
    constraint ck_spec_prixBaseSpec check (prixBaseSpec >= 0)
);

create table LesRepresentations (
    dateRep date primary key,
    promoRep decimal (4,2) not null,
    noSpec integer not null,
    constraint ck_rep_promoRep check (promoRep >= 0 and promoRep <=1),
    constraint fk_noSpec foreign key (noSpec)
    references LesSpectacles(noSpec)
);

create table TypeZones (
    catZone varchar (50) primary key,
    tauxZone decimal (4,2) not null,
    constraint ck_pl_tauxZone check (tauxZone >= 0),
    constraint ck_pl_cat check (catZone in ('orchestre', 'balcon', 'poulailler'))
);

create table LesZones (
    noZone integer primary key,
    catZone varchar (50) not null,
    constraint ck_pl_noZone check (noZone > 0),
    constraint fk_typZ foreign key (catZone) references TypeZones(catZone)
);

create table LesPlaces (
    noPlace integer,
    noRang integer,
    noZone integer not null,
    constraint pk_pl_noP_noR primary key (noPlace, noRang),
    constraint ck_pl_noP check (noPlace > 0),
    constraint ck_pl_noR check (noRang > 0),
    constraint fk_LesPlaces foreign key (noZone)
    references LesZones(noZone)
);

create table NumeroDossier (
    noDossier integer primary key
);

create table LesReductions (
    typePers varchar (50) primary key,
    tarifReduit decimal (4,2) not null,
    constraint ck_pl_typeP check (typePers in ('ordinaire', 'adhérent', 'étudiant','scolaire', 'militaire', 'sénior'))
);

create table LesTickets (
    noTrans integer primary key,
    dateTrans date not null,
    noPlace integer not null,
    noRang integer not null,
    typePers varchar (50) not null,
    noDossier integer,
    dateRep date not null,
    constraint ck_pl_noP check (noPlace > 0),
    constraint ck_pl_noR check (noRang > 0),
    constraint ck_pl_noD check (noDossier > 0),
    constraint fk_dateRep foreign key (dateRep)
    references LesRepresentations(dateRep),
    constraint fk_noP_noR foreign key (noPlace,noRang)
    references LesPlaces(noPlace,noRang),
    constraint fk_typeP foreign key (typePers)
    references LesReductions(typePers),
    constraint fk_noD foreign key (noDossier)
    references NumeroDossier(noDossier)
);


-- TODO 1.4 : Créer une vue LesRepresentations ajoutant le nombre de places disponible et d'autres possibles attributs calculés.
create view [Salle] as
select nomSpec, dateRep, (20 - count(noTrans)) as nbPlaceDisponibles, count(noTrans) as nbPlacesOccupe
from LesSpectacles left join LesRepresentations using (noSpec)
left join LesVentes using (dateRep)
group by nomSpec, dateRep;

-- TODO 1.5 : Créer une vue  avec le noDos et le montant total correspondant.
create view [LesDossiers] as
select noDossier, count(noTrans) as nbTicket, sum(prixTicket) as prixDossier
from NumeroDossier join [LesVentes] using (noDossier)
GROUP BY noDossier;

-- Creation de la vue Vente avec le prix du ticket calculer
create view [LesVentes] as
SELECT noTrans, dateTrans, noPlace, noRang, typePers, noDossier, dateRep, (prixBaseSpec * (1-promoRep) * (1-tarifReduit) * tauxZone) AS prixTicket
FROM LesTickets LEFT JOIN LesRepresentations USING (dateRep)
LEFT JOIN LesPlaces USING (noplace, norang)
LEFT JOIN LesZones USING (noZone)
LEFT JOIN TypeZones USING (catZone)
LEFT JOIN LesReductions USING (typePers)
LEFT JOIN LesSpectacles USING (noSpec);

-- TODO 3.3 : Ajouter les éléments nécessaires pour créer le trigger (attention, syntaxe SQLite différent qu'Oracle)
-- voir le fichier v1_trigger.sql
