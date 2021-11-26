-- FAIS 1.3 : Créer les tables manquantes et modifier celles ci-dessous

create table LesSpectacles (
    noSpec integer not null,
    nomSpec varchar(50) not null,
    prixBaseSpec decimal (6,2) not null,
    constraint pk_rep_noSpec primary key (noSpec),
    constraint ck_rep_noSpec check (noSpec > 0),
    constraint ck_spec_prixBaseSpec check (prixBaseSpec >= 0)
);

create table LesRepresentations (
    dateRep date not null,
    promoRep decimal (4,2) not null,
    noSpec integer not null,
    constraint pk_rep_dateRep primary key ( dateRep),
    constraint ck_rep_noSpec check (noSpec > 0), --pas forcement nécessaire puisqu'il doit verifier qu'il est dans LesSpectacles mais au moins erreur plus précise
    constraint ck_rep_promoRep check (promoRep >= 0 and promoRep <=1),
    constraint fk_noSpec foreign key (noSpec)
    references LesSpectacles(noSpec)
);

create table LesZones (
    noZone integer not null,
    catZone varchar (50) not null,
    constraint pk_pl_noZ primary key (noZone),
    constraint ck_pl_noZone check (noZone > 0),
    constraint ck_pl_cat check (catZone in ('orchestre', 'balcon', 'poulailler'))
);

create table TypeZones (
    catZone varchar (50) not null,
    tauxZone decimal (4,2) not null,
    constraint pk_pl_catZ primary key (catZone),
    constraint ck_pl_tauxZone check (tauxZone >= 0),
    constraint ck_pl_cat check (catZone in ('orchestre', 'balcon', 'poulailler')),
    constraint fk_typZ foreign key (catZone)
    references LesZones(noZone)
);

create table LesPlaces (
    noPlace integer,
    noRang integer,
    noZone integer not null,
    constraint pk_pl_noP_noR primary key (noPlace, noRang),
    constraint ck_pl_noP check (noPlace > 0),
    constraint ck_pl_noR check (noRang > 0),
    constraint ck_pl_noZone check (noZone > 0), --PAS FORCEMENT NECESSAIRE ?
    constraint fk_LesPlaces foreign key (noZone)
    references LesZones(noZone)
);

create table NumeroDosssier (
    noDossier integer,
    constraint pk_pl_noP_noR primary key (noDossier)
);

create table LesReductions (
    typePers varchar (50) not null,
    tarifReduit decimal (4,2) not null,
    constraint pk_pl_LesReducs primary key (typePers),
    constraint ck_pl_typeP check (typePers in ('ordinaire', 'adhérent', 'étudiant','scolaire', 'militaire', 'sénior'))
);

create table LesVentes (
    noTrans integer,
    dateTrans date not null,
    prixTotal integer,
    noPlace integer,
    noRang integer,
    typePers varchar (50) not null,
    noDossier integer,
    dateRep date not null,
    constraint pk_pl_LesV primary key (noTrans),
    constraint ck_pl_PrixTot check (prixTotal > 0),
    constraint ck_pl_noP check (noPlace > 0),
    constraint ck_pl_noR check (noRang > 0),
    constraint ck_pl_typeP check (typePers in ('ordinaire', 'adhérent', 'étudiant','scolaire', 'militaire', 'sénior')), --PAS FORCEMENT
    constraint ck_pl_noD check (noDossier > 0),
    constraint fk_dateRep foreign key (dateRep)
    references LesRepresentations(dateRep),
    constraint fk_noP_noR foreign key (noPlace,noRang)
    references LesPlaces(noPlace,noRang),
    constraint fk_typeP foreign key (typePers)
    references LesRéductions(typePers),
    constraint fk_noD foreign key (noDossier)
    references LesDosssiers(noD)
);
-- TODOFAIS 1.4 : Créer une vue LesRepresentations ajoutant le nombre de places disponible et d'autres possibles attributs calculés.
create view Salle as
select nomSpec, dateRep, (500 - count(noTrans)) as nbPlaceDisponibles, count(noTrans) as nbPlacesOccupe
from lesVentes join LesRepresentations using (dateRep)
               join LesSpectacles using (noSpec);
-- TODOFAIS 1.5 : Créer une vue  avec le noDos et le montant total correspondant.
create view LesDossiers as
select noDossier, sum(prixTotal) as prixDossier
from numeroDossier join LesVentes using (noDossier);


-- TODO 3.3 : Ajouter les éléments nécessaires pour créer le trigger (attention, syntaxe SQLite différent qu'Oracle)