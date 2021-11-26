-- TODO 1.3 : Créer les tables manquantes et modifier celles ci-dessous
create table LesRepresentations (
    daterep DATE PRIMARY KEY,
    promorep DECIMAL (4, 2) NOT NULL,
    CONSTRAINT ck_rep_promorep CHECK (
        promorep >= 0
        AND promorep <= 1
    )
);

CREATE TABLE LESSPECTACLES(
    nospec INT PRIMARY KEY,
    nomspec VARCHAR (50) NOT NULL,
    prixbasespec DECIMAL (6, 2) NOT NULL,
    CONSTRAINT ck_spec_nospec CHECK (nospec > 0),
    CONSTRAINT ck_spec_prixbasespec CHECK (prixbasespec >= 0)
);

create table LESVENTES (
    notrans int primary key,
    datetrans date NOT NULL,
    prixticket float NOT NULL,
    constraint ck_vente_prixticket check (prixticket >= 0)
);

CREATE table LESPLACES(
    noplace INT,
    norang int,
    CONSTRAINT pk_places_noplace_norang PRIMARY KEY (noplace, norang)
);

create table LesZones(
    noZones in PRIMARY KEY,
    constraint ck_zn_noZones CHECK (noZones > 0)
);

create table LESREPRESENTATION (
    daterep DATE PRIMARY KEY,
    promorep DECIMAL (4, 2) NOT NULL,
    CONSTRAINT ck_rep_promorep CHECK (
        promorep >= 0
        AND promorep <= 1
    )
);

create table LESREDUCTIONS(
    typepers varchar(20) PRIMARY KEY,
    tarifreduit DECIMAL (4, 2) NOT NULL,
    constraint ck_reduc_typepers check (
        catZone in (
            'ordinaire',
            'adhérent',
            'étudiant',
            'scolaire',
            'militaire',
            'sénior'
        )
    )
);
-- TODO 1.4 : Créer une vue LesRepresentations ajoutant le nombre de places disponible et d'autres possibles attributs calculés.
-- TODO 1.5 : Créer une vue  avec le noDos et le montant total correspondant.
-- TODO 3.3 : Ajouter les éléments nécessaires pour créer le trigger (attention, syntaxe SQLite différent qu'Oracle)