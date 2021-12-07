import sqlite3
from utils import display
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import QDateTime, QEventLoop
import datetime
from PyQt5 import uic


class AppGestRep(QDialog):
    """
    Fenêtre de gestion des représentations : ajout, modification, suppression
    """

    # Création d'un signal destiné à être émis lorsque la table est modifiée
    changedValue = pyqtSignal()

    # on prévoit les variables pour acceuillir les fenetres supplementaires
    fct_verif_supp_dialog = None
    fct_ajout_spectacle_dialog = None

    # On initialise la selection des lignes pour affiche une erreur si aucune ligne n'est slectionner
    selectedLines = None

    # booleen si on ne veut plus afficher la fenêtre de prevention avant suppression
    prevent_delete = True

    def __init__(self, data: sqlite3.Connection):
        super(QDialog, self).__init__()
        self.ui = uic.loadUi("gui/Gest_Rep.ui", self)
        self.data = data
        self.refreshResult()

    # Fonction de mise à jour de l'affichage
    @pyqtSlot()
    def refreshResult(self):
        try:
            cursor = self.data.cursor()
            result = cursor.execute(
                "SELECT nomSpec, DateRep, PrixBaseSpec, promoRep \
              FROM LesSpectacles JOIN LesRepresentations USING (noSpec)"
            )
        except Exception as e:
            self.ui.tableGestRep.setRowCount(0)
            display.refreshLabel(
                self.ui.label_table,
                "Impossible d'afficher les résultats : " + repr(e),
            )
        else:
            i = display.refreshGenericData(self.ui.tableGestRep, result)
            self.initComboBox()
            self.initTimeDate()
            if i == 0:
                display.refreshLabel(
                    self.ui.label_table, "Aucune représentation n'est programmé"
                )

    # initialisation du menu deroulant
    def initComboBox(self):
        self.NameList = []
        cursor = self.data.cursor()
        cursor.execute("SELECT DISTINCT nomSpec FROM LesSpectacles")
        res = cursor.fetchall()
        res.insert(0, ("",))
        self.CurrentName.clear()
        for item in res:
            self.NameList.append(item[0])
            self.CurrentName.addItem(item[0])

    def initTimeDate(self):
        datetime_object = str(datetime.datetime.now())
        date = datetime_object.split(" ")[0].split("-")
        time = datetime_object.split(" ")[1].split(":")
        self.CurrentTimeEdit.setDateTime(
            datetime.datetime(
                int(date[0]), int(date[1]), int(date[2]), int(time[0]), int(time[1])
            )
        )

    # lorsque qu'une case est selectionner alors on recupere les elements de la ligne
    def selectedLine(self):
        display.refreshLabel(self.ui.label_modif, "");
        self.selectedLines = sorted(
            set(
                index.row()
                for index in self.ui.tableGestRep.selectionModel().selectedIndexes()
            )
        )
        if len(self.selectedLines) > 0:
            self.selectedNom = self.ui.tableGestRep.item(
                self.selectedLines[0], 0
            ).text()
            self.selectedDate = self.ui.tableGestRep.item(
                self.selectedLines[0], 1
            ).text()
            self.selectedPrix = self.ui.tableGestRep.item(
                self.selectedLines[0], 2
            ).text()
            self.selectedPromo = self.ui.tableGestRep.item(
                self.selectedLines[0], 3
            ).text()
            self.refreshModif()

    def refreshModif(self):
        self.CurrentName.setCurrentIndex(self.NameList.index(self.selectedNom))
        timedate = self.selectedDate.split(" ")
        date = timedate[0].split("/")
        time = timedate[1].split(":")
        self.CurrentTimeEdit.setDateTime(
            datetime.datetime(
                int(date[2]), int(date[1]), int(date[0]), int(time[0]), int(time[1])
            )
        )
        self.CurrentPrice.setValue(float(self.selectedPrix))
        self.CurrentPromotion.setValue(float(self.selectedPromo) * 100)

    #################################################################################################
    # gestion des bouton
    #################################################################################################

    # en cas de clic sur le bouton ajouter
    def addRep(self):
        # Recuperation des valeurs à ajouter
        self.newNom = self.ui.CurrentName.currentText().strip()
        self.newDate = self.ui.CurrentTimeEdit.dateTime().toString(
            self.CurrentTimeEdit.displayFormat()
        )
        self.newPromo = self.ui.CurrentPromotion.value() / 100

        # Verifications des contraintes pour les nouvelles valeurs
        # Spectacles
        if not self.newNom:
            self.insertSpectacle = False
            self.newNom = self.Creation_Spectacles()
        else:
            self.insertSpectacle = True

        if self.insertSpectacle:
            # Date de la Representation
            if hasattr(self, "selectedDate"):
                if self.newDate != self.selectedDate:
                    self.addRepNext()
                else:
                    display.refreshLabel(self.ui.label_modif, "un spectacle utilise déjà cette horaire")
            else:
                self.addRepNext()

    def addRepNext(self):
        if self.VerifDateRep():
            if self.insertSQL(self.newDate, str(self.newPromo), self.getNoSpec()):
                self.selectedLines = None  # deselection des lignes
                self.refreshResult()  # on met à jour la fenetre pour avoir la nouvelle entree d'afficher

    def insertSQL(self, date=None, promo=None, noSpec=None):
        display.refreshLabel(self.ui.label_modif, "")
        try:
            cursor = self.data.cursor()
            cursor.execute(
                "INSERT INTO LesRepresentations VALUES (?, ?, ?)", [date, promo, noSpec]
            )
        except Exception as e:
            display.refreshLabel(
                self.ui.label_modif, "Erreur lors de l'insertion dans la table"
            )
            print(repr(e))
            return False
        else:
            self.data.commit()
            self.changedValue.emit()
            return True

    # en cas de clic sur le bouton modifier
    def modifRep(self):
        if self.selectedLines is not None:
            # Recuperation des valeurs à ajouter
            self.newNom = self.ui.CurrentName.currentText().strip()
            self.newDate = self.ui.CurrentTimeEdit.dateTime().toString(
                self.CurrentTimeEdit.displayFormat()
            )
            self.newPromo = self.ui.CurrentPromotion.value() / 100

            if self.Modification():
                if not self.newNom:
                    self.newNom = self.Creation_Spectacles()
                try:
                    cursor = self.data.cursor()
                    cursor.execute(
                        "DELETE FROM LesRepresentations WHERE noSpec = ? and dateRep = ? and promoRep = ?",
                        [
                            self.getNoSpec(self.selectedNom),
                            self.selectedDate,
                            str(self.selectedPromo),
                        ],
                    )
                except Exception as e:
                    display.refreshLabel(
                        self.ui.label_modif,
                        "Impossible de modifier cette représentation, veuillez réessayer !",
                    )
                    print(repr(e))
                else:
                    self.data.commit()  # on commit la suppression
                    self.changedValue.emit()
                    print("Delete complete")
                    try:
                        cursor.execute(
                            "INSERT INTO LesRepresentations VALUES (?, ?, ?)",
                            [
                                self.newDate,
                                str(self.newPromo),
                                self.getNoSpec(self.newNom),
                            ],
                        )
                    except Exception as e:
                        display.refreshLabel(
                            self.ui.label_modif,
                            "Impossible de modifier cette représentation",
                        )
                        cursor.execute(
                            "INSERT INTO LesRepresentations VALUES (?, ?, ?)",
                            [
                                self.selectedDate,
                                str(self.selectedPromo),
                                self.getNoSpec(self.selectedNom),
                            ],
                        )
                        self.data.commit()
                        self.changedValue.emit()
                    else:
                        self.data.commit()
                        self.changedValue.emit()
                        self.selectedLines = None
                        self.refreshResult()
            else:
                display.refreshLabel(
                    self.ui.label_modif, "Aucunes modifications à faire"
                )
        else:
            display.refreshLabel(self.ui.label_modif, "Veuillez sélectionner une entrée")

    # en cas de clic sur le bouton supprimer
    def deleteRep(self):
        display.refreshLabel(self.ui.label_modif, "")
        if self.selectedLines is None:
            display.refreshLabel(
                self.ui.label_modif,
                "Veuillez selectionner une ou plusieurs ligne(s) à supprimer !",
            )
        else:
            for row in self.selectedLines:
                cursor = self.data.cursor()
                cursor.execute(
                    "SELECT noSpec FROM LesSpectacles WHERE nomSpec = ?",
                    (self.ui.tableGestRep.item(row, 0).text(),),
                )
                delete_number = cursor.fetchall()
                if self.prevent_delete:
                    self.openVerifSupp(
                        self.ui.tableGestRep.item(row, 0).text(),
                        self.ui.tableGestRep.item(row, 1).text(),
                        self.ui.tableGestRep.item(row, 3).text(),
                    )
                    if self.response == 1:
                        result = cursor.execute(
                            "DELETE FROM LesRepresentations WHERE noSpec = ? and dateRep = ? and promorep = ?",
                            [
                                delete_number[0][0],
                                self.ui.tableGestRep.item(row, 1).text(),
                                self.ui.tableGestRep.item(row, 3).text(),
                            ],
                        )
                else:
                    result = cursor.execute(
                        "DELETE FROM LesRepresentations WHERE noSpec = ? and dateRep = ? and promorep = ?",
                        [
                            delete_number[0][0],
                            self.ui.tableGestRep.item(row, 1).text(),
                            self.ui.tableGestRep.item(row, 3).text(),
                        ],
                    )
            self.data.commit()
            self.refreshResult()
            self.selectedLines = None  # On vient de supprimer la ligne donc, elle n'est plus selectionnée

    # Recuperation du numero du spectacle en fontion du nom a ajouter
    def getNoSpec(self, nom=None):
        cursor = self.data.cursor()
        cursor.execute(
            "SELECT noSpec FROM LesSpectacles WHERE nomSpec = ?", (self.newNom,)
        )
        return sorted(set(index[0] for index in cursor.fetchall()))[0]

    # Verification de la date de representation
    def VerifDateRep(self):
        cursor = self.data.cursor()
        cursor.execute(
            "SELECT dateRep FROM LesRepresentations WHERE dateRep = ?",
            [str(self.newDate)],
        )
        if len(sorted(set(item[0] for item in cursor.fetchall()))) != 0:
            display.refreshLabel(
                self.ui.label_modif,
                "Cette programmation est déjà utilisé par un autre spectacle",
            )
            return False
        # Recuperation des date de representations pour un meme spectacles
        cursor.execute(
            "SELECT dateRep FROM lesRepresentations WHERE noSpec = ?",
            [str(self.getNoSpec())],
        )
        for day in sorted(set(item[0] for item in cursor.fetchall())):
            if day.split(" ")[0] == self.newDate.split(" ")[0]:
                display.refreshLabel(
                    self.ui.label_modif,
                    "Ce spectacle ne peut avoir plus d'une représetation le même jour",
                )
                return False
        # Si les dates respectent les conditions pour etre ajouter dans la table
        return True

    # Si comboBox vide lors de la modification ou ajout d'une entree
    def Creation_Spectacles(self):
        if self.fct_ajout_spectacle_dialog is not None:
            self.fct_ajout_spectacle_dialog.close()
        self.fct_ajout_spectacle_dialog = AppAjoutSpectacle(self.data)
        self.fct_ajout_spectacle_dialog.exec_()
        self.insertSpectacle = self.fct_ajout_spectacle_dialog.insert
        return self.fct_ajout_spectacle_dialog.spec

    # Affichage de la fenetre lors de la suppression
    def openVerifSupp(self, nomSpec, dateRep, promo):
        if self.fct_verif_supp_dialog is not None:
            self.fct_verif_supp_dialog.close()
        self.fct_verif_supp_dialog = AppVerifSupp(nomSpec, dateRep, promo)
        self.fct_verif_supp_dialog.exec_()
        self.response = self.fct_verif_supp_dialog.response
        self.prevent_delete = self.fct_verif_supp_dialog.prevent_delete

    #################################################################################################
    # Fonctions Conditionnel
    #################################################################################################

    def line_selected(self):
        return (
            self.selectedNom is not None
            and self.selectedDate is not None
            and self.selectedPromo is not None
        )

    def Modification(self):
        return self.NameNotPromo() or self.DateNotName() or self.PromoNotDate()

    def NameNotPromo(self):
        return (self.newNom != self.selectedNom) and not (
            self.newPromo != self.selectedPromo
        )

    def DateNotName(self):
        return not (self.newNom != self.selectedNom) and (
            self.newDate != self.selectedDate
        )

    def PromoNotDate(self):
        return not (self.newDate != self.selectedDate) and (
            self.newPromo != self.selectedPromo
        )

    #################################################################################################
    # Cloture des fenetres
    #################################################################################################

    def closeEvent(self, event):

        # On ferme les éventuelles fenêtres encore ouvertes
        if self.fct_verif_supp_dialog is not None:
            self.fct_verif_supp_dialog.close()
        if self.fct_ajout_spectacle_dialog is not None:
            self.fct_ajout_spectacle_dialog.close()

        # On laisse l'évènement de clôture se terminer normalement
        event.accept()


class AppAjoutSpectacle(QDialog):
    """
    Fenêtre de creation d'un nouveau spectacle
    """

    spec = ""
    insert = True

    def __init__(self, data: sqlite3.Connection):
        super(QDialog, self).__init__()
        self.ui = uic.loadUi("gui/fct_add_spec.ui", self)
        self.data = data
        display.refreshLabel(self.ui.label_error, "")

    @pyqtSlot()
    def addSpec(self):
        self.spec = self.ui.lineEditSpec.text().strip()
        self.prix = self.ui.doubleSpinBoxPrix.value()

        if len(self.spec) > 0:
            if not self.alreadyExist():
                try:
                    cursor = self.data.cursor()
                    cursor.execute(
                        "INSERT INTO LesSpectacles(nomSpec, prixBaseSpec) VALUES(?, ?)",
                        [self.spec, str(self.prix)],
                    )
                except Exception as e:
                    display.refreshLabel(
                        self.ui.label_error,
                        "Erreur lors de l'ajout du spectacle, veuillez réessayer !",
                    )
                    print(repr(e))
                else:
                    display.refreshLabel(
                        self.ui.label_error, "Spectacle ajouté avec succés"
                    )
                    self.data.commit()
                    self.close()
            else:
                display.refreshLabel(self.ui.label_error, "Ce nom existe déjà")
                self.insert = False
        else:
            display.refreshLabel(
                self.ui.label_error, "Impossible d'ajouter un nom de spectacle vide"
            )
            self.insert = False

    def alreadyExist(self):
        cursor = self.data.cursor()
        cursor.execute("SELECT nomSpec, prixBaseSpec FROM LesSpectacles")
        for item in cursor.fetchall():
            if item == (self.spec, str(self.prix)):
                return True
        return False


class AppVerifSupp(QDialog):
    """
    Fenêtre d'avertissement avant suppression
    """

    prevent_delete = True
    response = False

    def __init__(self, nomSpec, dateRep, promo):
        super(QDialog, self).__init__()
        self.ui = uic.loadUi("gui/dialogue_verif.ui", self)
        self.response = False
        self.answered = False
        display.refreshLabel(self.ui.label_nomRep, nomSpec)
        display.refreshLabel(
            self.ui.label_dateRep, "Date de la Représentation : " + dateRep
        )
        display.refreshLabel(
            self.ui.label_promoRep, "Promotion de la représentation : " + promo
        )

    def delete(self):
        self.response = True
        self.answered = True
        self.close()

    def always_delete(self):
        if self.prevent_delete:
            self.prevent_delete = False
        else:
            self.prevent_delete = True
