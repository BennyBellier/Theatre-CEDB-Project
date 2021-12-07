# Theatre-CEDB-Project

Projet d'informatisation d'un système de réservation de spectacle dans un thêatre.

---

Nous nous sommes basé sur le fichier "Theatre_UML.drawio.svg", pour construire notre base de données. Le fichier "Diagram_UML_après_implémentation.drawio.svg" représente notre base de données final qui ne contient pas de bug et les possibles nouvelles table ou vue créer.

## Triggers

Nous avons trois triggers :
 - trig_same_date : permet de vérifier que deux représentation ne sont pas à la même date.
 - trig_RepresentationObsolete : permet de vérifier que la représentation que l'on souhaite ajouté, n'est pas à une date antérieur à celle de l'ajout.
 - trig_PlaceOccupe : permet de vérifier qu'une place choisit n'est pas déjà occupé pour la même représentation.

## Gestion des représentations

Pour la gestion des représentations, nous avons trois possibilités : ajouter, supprimer et modifier. Tout d'abord le bouton ajouter permet de créer une nouvelle représentations. Il faut alors avant d'appuyer sur le bouton, renseigner les champs : "Nom", "Programmations", "Promotion". Si le champ "Nom" est laissé vide, une fenêtre va alors souvrir pour ajouter un nouveau spectacle.
Attention : il vous est impossible de créer une représentation avec une date antérieur, à la date à laquelle vous la créer (exemple : il est impossible de créer une représentation pour le 25 janvier 2021, si lorsque vous la créer vous êtes le 18 février 2021).

Pour utiliser le bouton modifier, vous devez selectionner la représentation a modifier dans la table puis de modifier c'est attributs sur la droite. Si les 3 champs sont modifié alors le bouton n'effectuera aucunes actions, car c'est une nouvelle représentations que vous voulez créer.

Si vous voulez supprimer une ou plusieurs représentations, il suffit de les selectionner dans la table et de cliquer sur supprimer. Une fenêtre s'ouvrira vous demendans de confirmer la suppression ou non.

## Gestion des réservations

---

# Todo List

- [x] CONCEPTION
  - [x] Question 1
    - [x] Identifier les DFs
    - [x] Commenter les hypothèses
    - [x] Proposition d'un schéma de relations BCNF
    - [x] Justifications **soigner**
  - [x] Question 2
    - [x] Réalisation du diagramme UML :
      - [x] Les classes (avec ids)
      - [x] les associations entre classes (noms et cardinalités)
      - [x] commentaire (hypothèses / contraintes à prendre en compte pour la transformation)
  - [x] Question 3
    - [x] Déductions du schéma relationnel
    - [x] Précision des :
      - [x] Relations
      - [x] Domaines
      - [x] Contraintes d'intégrités
      - [x] Possibles vues
- [x] IMPLÉMENTATION
  - [x] Question 4
    - [x] Partie 0
      - [x] Génération du projet
      - [x] Vérification code fournie
    - [x] Partie 1
      - [x] Réalisation des extensions du code fournie
      - [x] Créations des vues (avec attribues calculés + maj interface)
    - [x] Partie 2
      - [x] Créations nouvelles fenêtres dans l'interface
      - [x] Prise en compte des évenements associés à des nouvelles actions
    - [x] Partie 3
      - [x] Imaginations de nouvelles fonctionnalités de l'applications
      - [x] Proposition d'un **Trigger pertinent**
