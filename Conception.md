## Sujet

## Sujet

$V0\_LesRepresentations$ _(noSpec, dateRep, nomSpec, prixBaseSpec, promoRep, prixRep)_<br/>
/\*<s, d, n, pxb, prm, pxr> ∈ V0LesReprésentations ⇐⇒ d est la date d’une représentation pour le spectacle
s du nom n. Au prix de base pxb on peut lui appliquer un taux de promotion prm (entre 0 et 1) qui donne le prix de la representation pxr. \*/<br/>
$V0\_LesPlaces$ _(noPlace, noRang, noZone, catZone, tauxZone)_<br/>
/\* <p, r, z, c, t> ∈ V0LesPlaces ⇐⇒ la place de numéro p dans le rang r est dans la zone z. Les places de la
zone z sont dans la catégorie c. Une catégorie est associé à un taux t par rapport au prix de base. \*/


$LesSpectacles$ _(**noSpec**, nomSpec, prixBaseSpec)_<br/>
/\*<nS, nomS, pBS> ∈ LesSpectacles ⇐⇒ Le spectacle nomS est identifié par le numéro nS et à pour prix de base pBS. \*/<br/>

$LesRepresentations$ _(**dateRep**, noSpec, promoRep)_<br/>
/\*<dR, nS, prR> ∈ LesRepresentations ⇐⇒ Une représentation du spectacle numéro nS a lieu a la date dR et fait l'objet d'une promotion prR. \*/<br/>

$LesPlaces$ _(**noPlaces, noRang**, noZone)<br/>
/\*<noP, noR, noZ> ∈ LesPlaces ⇐⇒ La place noP du rang noR se situe dans la zone noZ. \*/<br/>

$LesZones$ _(**noZone**, catZone, tauxZone)<br/>
/\*<noZ, cZ, tZ> ∈ LesZones ⇐⇒ Chaque catégorie est représenté par une zone dans la salle. Ce taux est fixe pour l'ensemble
des spectacles et est en rapport avec le prix de base de ceux là. \*/<br/>

$LesVentes$ _(**noTrans**, dateTrans, noPlaces, noDossier, PrixTotal)<br/>
/\*<noT, dT, noP, noD, pT> ∈ LesVentes ⇐⇒ Le numéro de transaction noT possède une date de transaction dT. Si une seule place
est acheté alors noDossier = NULL et le prix de la transaction est le prix pT. Si plusieurs sont achetées alors noD est le numéro
du dossier regroupant toutes les places achetées et noP = NULL  \*/<br/>

$LesDossiers$ _(**noDossier**, noPlaces)<br/>
/\*<noT, noP> ∈ LesDossiers ⇐⇒ Le dossier noT contient toutes les places noP. \*/<br/>

$LesReductions$ _(**typePers**, tarifReduit)<br/>
/\*<tP, tR> ∈ LesReductions ⇐⇒ Le tarif réduit tR est réservé au personnes du type tP. \*/<br/>

---

### Dépendances fonctionnelles

**$Les Representations$**
noSpec -> nomSpec, prixBaseSpec<br/>
noSpec, dateRep -> promoRep<br/>
PrixBaseRep, promoRep -> prixRep<br/>

Il y a qu'une seul salle de représentation, donc on as la relation : DateRep -> noSpec. Hors, on a trouvé plus haut que la pair noSPec, dateRep est une clef. Et une partie de la clé ne peut pas donner l'autre partie.

**$Les Places$**
noZone -> catZone<br/>
catZone -> noZone<br/>
catZone -> tauxZone<br/>
noPlace, noRang -> noZone

On trouve un doublon, catZone et noZone, indique de manière différente la même chose.

**$Les Ventes$**
noTrans -> dateTrans, prixTotal, noPlaces, noDossier<br/>
noDossier -> noPlaces

**$Les Reductions$**
dateRep -> tauxRep<br/>
typePers -> tarifReduit

---

### Normalisation

**$Les Representations$**<br/>
LesSpectacles(**noSpec**, nomSpec, prixBaseSpec)<br/>
LesRepresentations(**dateRep**, noSpec, promoRep)

**$Les Places$**<br/>
LesPlaces(**noPlace, noRang**, noZone)<br/>
LesZones(**noZone**, catZone, tauxZone)

**$Les Ventes$**<br/>
LesVentes(**noTrans**, dateTrans, noPlaces, noDossier, PrixTotal)<br/>
LesDossiers(**noDossier**, noPlaces)

**$Les Reductions$**<br/>
LesReductions(**typePers**, tarifReduit)<br/>

|     Relations      | 1NF | 2NF | 3NF | BCNF |
| :----------------: | :-: | :-: | :-: | :--: |
|   LesSpectacles    |  X  |  X  |  X  |  X   |
| LesRepresentations |  X  |  X  |  X  |  X   |
|     LesPlaces      |  X  |  X  |  X  |  X   |
|      LesZones      |  X  |  X  |  X  |  X   |
|     LesVentes      |  X  |  X  |  X  |  X   |
|    LesDossiers     |  X  |  X  |  X  |  X   |
