import sqlite3
from utils import display
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import QTime
from PyQt5 import uic


class AppGestRep(QDialog):
    """
    Fenêtre de gestion des représentations : ajout, modification, suppression
    """

    def __init__(self, data: sqlite3.Connection):
        super(QDialog, self).__init__()
        self.ui = uic.loadUi("gui/Gest_Rep.ui", self)
        self.data = data
        self.refreshResult()

    # Fonction de mise à joru de l'affichage
    @pyqtSlot()
    def refreshResult(self):
        display.refreshLabel(self.ui.label_gest_rep, "")
        try:
            cursor = self.data.cursor()
            result = cursor.execute(
                "SELECT nomSpec, DateRep, PrixBaseSpec, promoRep \
              FROM LesSpectacles JOIN LesRepresentations USING (noSpec)"
            )
        except Exception as e:
            self.ui.tableRepVide.setRowCount(0)
            display.refreshLabel(
                self.ui.label_gest_rep,
                "Impossible d'afficher les résultats : " + repr(e),
            )
        else:
            i = display.refreshGenericData(self.ui.tableGestRep, result)
            self.initComboBox()
            if i == 0:
                display.refreshLabel(self.ui.label_gest_rep, "Aucun représentation n'est programmé")

    # initialisation du menu deroulant
    def initComboBox(self):
        self.NameList = []
        cursor = self.data.cursor()
        cursor.execute("SELECT DISTINCT nomSpec FROM LesSpectacles")
        res = cursor.fetchall()
        print(res)
        res.insert(0, ("",))
        for item in res:
            self.NameList.append(item[0])
            self.CurrentName.addItem(item[0])
        print(self.NameList)

    # lorsque qu'une case est selectionner alors on recupere les elements de la ligne
    def selectedLine(self):
        rows = sorted(set(index.row() for index in self.ui.tableGestRep.selectedIndexes()))
        self.nom = self.ui.tableGestRep.item(rows[0], 0).text()
        self.date = self.ui.tableGestRep.item(rows[0], 1).text()
        self.prix = self.ui.tableGestRep.item(rows[0], 2).text()
        self.promo = self.ui.tableGestRep.item(rows[0], 3).text()
        print(self.nom, self.date, self.prix, self.promo)
        self.refreshModif()

    def refreshModif(self):
        self.CurrentName.setCurrentIndex(self.NameList.index(self.nom))
        # datetime = self.date.split(' ')
        self.CurrentTimeEdit.setDateTime(QTime.fromString(self.date, "dd/mm/yyyy hh:mm"))
        # self.currentDate.setTime(QTime.fromString(datetime[1], "hh:00"))
        self.CurrentPrice.setValue(self.prix)
        self.CurrentPromotion.setValue(self.promo)



    #################################################################################################
    # gestion des bouton
    #################################################################################################

    # en cas de clic sur le bouton ajouter
    def addRep(self):
        pass

    # en cas de clic sur le bouton modifier
    def modifRep():
        pass

    # en cas de clic sur le bouton supprimer
    def deleteRep():
        pass

    #################################################################################################
    # Cloture des fenetres
    #################################################################################################

    def closeEvent(self, event):

        # On ferme les éventuelles fenêtres encore ouvertes

        # On laisse l'évènement de clôture se terminer normalement
        event.accept()