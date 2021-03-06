CREATE TABLE V0_LESREPRESENTATIONS(
  nospec integer NOT NULL,
  nomspec VARCHAR (50) NOT NULL,
  daterep DATE NOT NULL,
  promorep DECIMAL (4, 2) NOT NULL,
  prixbasespec DECIMAL (6, 2) NOT NULL,
  prixrep DECIMAL (6, 2) NOT NULL,
  CONSTRAINT pk_rep_nospec_daterep PRIMARY KEY (nospec, daterep),
  CONSTRAINT ck_rep_nospec CHECK (nospec > 0),
  CONSTRAINT ck_spec_prixbasespec CHECK (prixbasespec >= 0),
  CONSTRAINT ck_spec_prixbasespec CHECK (prixrep >= 0),
  CONSTRAINT ck_rep_promorep CHECK (
    promorep >= 0
    AND promorep <= 1
  )
);
CREATE TABLE V0_LESPLACES(
  noplace integer,
  norang integer,
  nozone integer NOT NULL,
  catzone VARCHAR (50) NOT NULL,
  tauxzone DECIMAL (4, 2) NOT NULL,
  CONSTRAINT pk_pl_nop_nor PRIMARY KEY (nozone, noplace, norang),
  CONSTRAINT ck_pl_nop CHECK (noplace > 0),
  CONSTRAINT ck_pl_nor CHECK (norang > 0),
  CONSTRAINT ck_pl_nozone CHECK (nozone > 0),
  CONSTRAINT ck_pl_tauxzone CHECK (tauxzone >= 0),
  CONSTRAINT ck_pl_cat CHECK (
    catzone IN ('orchestre', 'balcon', 'poulailler')
  )
);