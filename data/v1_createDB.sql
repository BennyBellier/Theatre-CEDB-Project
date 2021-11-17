-- TODO 1.3 : Créer les tables manquantes et modifier celles ci-dessous
create table LesRepresentations (
    noSpec integer not null,
    nomSpec varchar(50) not null,
    dateRep date not null,
    promoRep decimal (4,2) not null,
    prixBaseSpec decimal (6,2) not null,
    prixRep decimal (6,2) not null,
    constraint pk_rep_noSpec_dateRep primary key (noSpec, dateRep),
    constraint ck_rep_noSpec check (noSpec > 0),
    constraint ck_spec_prixBaseSpec check (prixBaseSpec >= 0),
    constraint ck_spec_prixBaseSpec check (prixRep >= 0),
    constraint ck_rep_promoRep check (promoRep >= 0 and promoRep <=1)
);

create table LesPlaces (
    noPlace integer,
    noRang integer,
    noZone integer not null,
    catZone varchar (50) not null,
    tauxZone decimal (4,2) not null,
    constraint pk_pl_noP_noR primary key (noZone, noPlace, noRang),
    constraint ck_pl_noP check (noPlace > 0),
    constraint ck_pl_noR check (noRang > 0),
    constraint ck_pl_noZone check (noZone > 0),
    constraint ck_pl_tauxZone check (tauxZone >= 0),
    constraint ck_pl_cat check (catZone in ('orchestre', 'balcon', 'poulailler'))
);
-- TODO 1.4 : Créer une vue LesRepresentations ajoutant le nombre de places disponible et d'autres possibles attributs calculés.
-- TODO 1.5 : Créer une vue  avec le noDos et le montant total correspondant.
-- TODO 3.3 : Ajouter les éléments nécessaires pour créer le trigger (attention, syntaxe SQLite différent qu'Oracle)