## Sujet

$V0\_LesRepresentations$ _(noSpec, dateRep, nomSpec, prixBaseSpec, promoRep, prixRep)_
<s, d, n, pxb, prm, pxr>∈V0 LesRepr ́esentations ⇐⇒d est la date d’une repr ́esentation pour le spectacle
s du nom n. Au prix de base pxb on peut lui appliquer un taux de promotion prm (entre 0 et 1) qui donne le prix
de la repr ́esentation pxr
$V0\_LesPlaces$ _(noPlace, noRang, noZone, catZone, tauxZone)_
/_ <p, r, z, c, t>∈V0 LesPlaces ⇐⇒la place de num ́ero p dans le rang r est dans la zone z. Les places de la
zone z sont dans la cat ́egorie c. Une cat ́egorie est associ ́e `a un taux t par rapport au prix de base. _/

### Dépendances fonctionnelles

**$Les Representations$**
noSpec -> nomSpec, prixBaseSpec
noSpec, dateRep -> promoRep
PrixBaseRep, promoRep -> prixRep

Il y a qu'une seul salle de représentation, donc on as la relation : DateRep -> noSpec. Hors, on a trouvé plus haut que la pair noSPec, dateRep est une clef. Et une partie de la clé ne peut pas donner l'autre partie.

**$Les Places$**
noZone -> catZone
catZone -> noZone,
catZone -> tauxZone
noPlace, noRang -> noZone

On trouve un doublon, catZone et noZone, indique de manière différente la même chose.

**$Les Ventes$**
noTrans -> dateTrans, prixTotal, noPlaces, noDossier
noDossier -> noPlaces

**$Les Reductions$**
dateRep -> tauxRep
typePers -> tarifReduit

---

### Normalisation

**$Les Representations$**
LesSpectacles(**noSpec**, nomSpec, prixBaseSpec)
lesRepresentations(**dateRep**, noSpec, promoRep)

**$Les Places$**
LesPlaces(**noPlace, NoRang**, noZone)
LesZones(**noZone**, catZone, tauxZone)

**$Les Ventes$**
LesVentes(**noTrans**, dateTrans, noPlaces, noDossier, PrixTotal)
LesDossiers(**noDossier**, noPlaces)

**$Les Reductions$\*\*
LesReductions(**typePers\*\*, tarifReduit)
