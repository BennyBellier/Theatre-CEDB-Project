
import sqlite3
from utils import display
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSlot
from PyQt5 import uic

# Classe permettant d'afficher la fonction à compléter 1
class AppFctRepVide(QDialog):

    # Constructeur
    def __init__(self, data:sqlite3.Connection):
        super(QDialog, self).__init__()
        self.ui = uic.loadUi("gui/fct_rep_vide.ui", self)
        self.data = data
        self.refreshResult()

    # Fonction de mise à joru de l'affichage
    @pyqtSlot()
    def refreshResult(self):
        display.refreshLabel(self.ui.label_rep_vide, "")
        try:
            cursor = self.data.cursor()
            result = cursor.execute(
                "SELECT nomSpec, DateRep, PrixBaseSpec \
                  FROM LesSpectacles \
                  JOIN LesRepresentations USING (noSpec) \
                  JOIN Salle USING (nomSpec, dateRep) \
                  WHERE nbPlacesOccupe = 0")
        except Exception as e:
            self.ui.tableRepVide.setRowCount(0)
            display.refreshLabel(self.ui.label_rep_vide, "Impossible d'afficher les résultats : " + repr(e))
        else:
            i = display.refreshGenericData(self.ui.tableRepVide, result)
            self.ui.lcdNumberRep.display(i)
            if i == 0:
                display.refreshLabel(self.ui.label_rep_vide, "Aucun résultat")