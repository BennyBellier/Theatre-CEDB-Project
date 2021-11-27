
import sqlite3
from utils import display
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSlot
from PyQt5 import uic

# Classe permettant d'afficher la fonction à compléter 2
class AppFctComp2Partie1(QDialog):



    # Constructeur
    def __init__(self, data:sqlite3.Connection):
        super(QDialog, self).__init__()
        self.ui = uic.loadUi("gui/fct_comp_2.ui", self)
        self.data = data
        #INIT COMBO BOX:
        cursor = data.cursor()
        cursor.execute("SELECT DISTINCT catZone FROM TypeZones")
        res = cursor.fetchall()
        for raw in res:
            self.comboBox.addItem(raw[0])


    # Fonction de mise à jour de l'affichage
    @pyqtSlot()
    def refreshResult(self):
        # TODO 1.2 : fonction à modifier pour remplacer la zone de saisie par une liste de valeurs issues de la BD une fois le fichier ui correspondant mis à jour
        display.refreshLabel(self.ui.label_fct_comp_2, "")
        #geek_list = ["Geek", "Geeky Geek", "Legend Geek", "Ultra Legend Geek"]
         # adding list of items to combo box

        #self.ui.combo_box.setEditable(True)


        if not self.ui.comboBox.currentText().strip():
            self.ui.table_fct_comp_2.setRowCount(0)
            display.refreshLabel(self.ui.label_fct_comp_2, "Veuillez indiquer un nom de catégorie")
        else:
            try:

                cursor = self.data.cursor()
                result = cursor.execute(
                    "SELECT noPlace, noRang, noZone, tauxZone FROM LesPlaces JOIN LesZones USING (noZone) JOIN TypeZones USING (catZone) WHERE catZone = ?",
                    [self.ui.comboBox.currentText().strip()])
            except Exception as e:
                self.ui.table_fct_comp_2.setRowCount(0)
                display.refreshLabel(self.ui.label_fct_comp_2, "Impossible d'afficher les résultats : " + repr(e))
            else:
                i = display.refreshGenericData(self.ui.table_fct_comp_2, result)
                if i == 0:
                    display.refreshLabel(self.ui.label_fct_comp_2, "Aucun résultat")