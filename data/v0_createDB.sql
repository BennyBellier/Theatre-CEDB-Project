create table V0_LesRepresentations (
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

create table V0_LesPlaces (
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
