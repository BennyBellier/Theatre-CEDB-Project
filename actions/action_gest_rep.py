import sqlite3
from utils import display
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import QDateTime
import datetime
from PyQt5 import uic


class AppGestRep(QDialog):
    """
    Fenêtre de gestion des représentations : ajout, modification, suppression
    """

    # on prévoit les variables pour acceuillir les fenetres supplementaires
    fct_verif_supp = None

    # valeur pour effectuer le Ctrl + z
    ancientNom = ""
    ancientDate = ""
    ancientPrix = 0
    ancientPromo = 0

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
                display.refreshLabel(
                    self.ui.label_gest_rep, "Aucun représentation n'est programmé"
                )

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
        rows = sorted(
            set(index.row() for index in self.ui.tableGestRep.selectedIndexes())
        )
        self.selectedNom = self.ui.tableGestRep.item(rows[0], 0).text()
        self.selectedDate = self.ui.tableGestRep.item(rows[0], 1).text()
        self.selectedPrix = self.ui.tableGestRep.item(rows[0], 2).text()
        self.selectedPromo = self.ui.tableGestRep.item(rows[0], 3).text()
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
        self.CurrentPromotion.setValue(float(self.selectedPromo))

    #################################################################################################
    # gestion des bouton
    #################################################################################################

    # en cas de clic sur le bouton ajouter
    def addRep(self):
        pass

    # en cas de clic sur le bouton modifier
    def modifRep(self):
        pass

    # en cas de clic sur le bouton supprimer
    def deleteRep(self):
        pass

    # en cas d'appuie sur les toucher Ctrl + z
    def CtrlZ(self):
        pass

    #################################################################################################
    # Cloture des fenetres
    #################################################################################################

    def closeEvent(self, event):

        # On ferme les éventuelles fenêtres encore ouvertes
        if self.fct_verif_supp is not None:
            self.fct_verif_supp.close()

        # On laisse l'évènement de clôture se terminer normalement
        event.accept()
