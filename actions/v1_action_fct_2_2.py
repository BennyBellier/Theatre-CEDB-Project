import sqlite3
from utils import display
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSlot
from PyQt5 import uic

# Classe permettant d'afficher la fenêtre de visualisation des données
class AppFct2Partie2(QDialog):

    def __init__(self, data:sqlite3.Connection):
        super(QDialog, self).__init__()
        self.ui = uic.loadUi("gui/fct_2_2.ui", self)
        self.data = data
        self.refreshResult()

    @pyqtSlot()
    def refreshResult(self):
        display.refreshLabel(self.ui.label_fct_2_2, "")
        try:
            cursor = self.data.cursor()
            result = cursor.execute("SELECT nomSpec, dateRep, nbPlacesOccupe as nbPlacesReserve FROM LesSpectacles JOIN Salle USING (nomSpec)")
        except Exception as e:
            self.ui.table_fct_2_2.setRowCount(0)
            display.refreshLabel(self.ui.label_fct_2_2, "Impossible d'afficher les résultats : " + repr(e))
        else:
            display.refreshGenericData(self.ui.table_fct_2_2, result)

