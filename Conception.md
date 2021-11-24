## Sujet

$V0\_LesRepresentations$ _(noSpec, dateRep, nomSpec, prixBaseSpec, promoRep, prixRep)_<br/>
/\*<s, d, n, pxb, prm, pxr> ∈ V0LesReprésentations ⇐⇒ d est la date d’une représentation pour le spectacle
s du nom n. Au prix de base pxb on peut lui appliquer un taux de promotion prm (entre 0 et 1) qui donne le prix de la representation pxr. \*/<br/>
$V0\_LesPlaces$ _(noPlace, noRang, noZone, catZone, tauxZone)_<br/>
/\* <p, r, z, c, t> ∈ V0LesPlaces ⇐⇒ la place de numéro p dans le rang r est dans la zone z. Les places de la
zone z sont dans la catégorie c. Une catégorie est associé à un taux t par rapport au prix de base. \*/

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
lesRepresentations(**dateRep**, noSpec, promoRep)

**$Les Places$**<br/>
LesPlaces(**noPlace, NoRang**, noZone)<br/>
LesZones(**noZone**, catZone)<br/>
TypeZones(**catZone**, tauxZone)

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

$LesSpectacles$ _(**noSpec**, nomSpec, prixBaseSpec)_<br/>
/\*<nS, nomS, pBS> ∈ LesSpectacles ⇐⇒ Le spectacle nomS est identifié par le numéro nS et à pour prix de base pBS. \*/<br/>

$LesRepresentations$ _(**dateRep**, promoRep, noSpec )_<br/>
/\*<dR, prR, nS,> ∈ LesRepresentations ⇐⇒ Une représentation du spectacle numéro nS a lieu a la date dR et fait l'objet d'une promotion prR. \*/<br/>

$LesVentes$ _(**noTrans**, dateTrans, PrixTotal, noPlaces, noRang, typeP, noDossier, dateRep)_<br/>
/\*<noT, dT, pT, noP, noR, tP, noD,  dR> ∈ LesVentes ⇐⇒ Le numéro de transaction noT possède une date de transaction dT. Si une seule place est acheté pour la représentation qui a lieu a la date dR alors noDossier = NULL et le prix de la transaction est le prix pT. Si plusieurs sont achetées alors noD est le numéro du dossier regroupant toutes les places achetées en même temps des placeset noP = NULL. noR correspond au rang de chaque place et tP est le type de personne pour qui la place noP a été acheté.  \*/<br/>



$LesPlaces$ _(**noPlaces, noRang**, noZone)_<br/>
/\*<noP, noR, noZ> ∈ LesPlaces ⇐⇒ La place noP du rang noR se situe dans la zone noZ. \*/<br/>

$LesZones$ _(**noZone**, catZone)_<br/>
/\*<noZ, cZ> ∈ LesZones ⇐⇒ Chaque catégorie cZ est représenté par un numéro de zone noZ dans la salle.\*/<br/>

$TypesZones$ _(**catZone**, tauxZone)_ <br/>
/\*<cZ, tZ> ∈ TypesZones ⇐⇒ Chaque taux tZ correspond à une catégorie de zone cZ dans la salle.\*/<br/>



$LesDossiers$ _(**noDossier**, noPlaces, noRang, typeP)_<br/>
/\*<noD, noP, noR, typeP> ∈ LesDossiers ⇐⇒ Lors d'une transaction, le dossier noD contient toutes les places noP situé au rang noR en fonction du type de la personne typeP. \*/<br/>

$LesReductions$ _(**typePers**, tarifReduit)_<br/>
/\*<tP, tR> ∈ LesReductions ⇐⇒ Le tarif réduit tR est réservé au personnes du type tP. \*/<br/>


LesReprésentation[noSpec] ⊆ LesSpectacles[noSpec]
LesVentes[dateRep] ⊆ LesRepresentations[dateRep]
LesVentes[noPlaces, noRang] ⊆ LesPlaces[noPlace,noRang] 
LesDossiers[noDossier] ⊆ LesVentes[noDossier]
LesPlaces[noZone] ⊆ LesZones[noZone]
LesVentes[typeP] ⊆ LesRéductions[typeP]















