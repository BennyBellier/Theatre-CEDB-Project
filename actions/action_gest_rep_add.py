import sqlite3
from utils import display
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSlot
from PyQt5 import uic

class AppGestRep_add(QDialog):

    def __init__(self, data: sqlite3.Connection):
        super(QDialog, self).__init__()
        self.ui = uic.loadUi("gui/Gest_Rep_add.ui", self)
        self.data = data

    def refreshResult(self):
        display.refreshLabel(self.ui.label_res, "")
        i = 0
        try:
            cursor = self.data.cursor()
            if not self.ui.lineEdit_date.text().strip() or not self.ui.lineEdit_promo.text().strip() or not self.ui.lineEdit_num.text().strip() :
                i = 1
            result = cursor.execute("INSERT INTO LesRepresentations(dateRep, promoRep, noSpec) VALUES ( ?, ?, ?)",
                       [self.ui.lineEdit_date.text().strip(), self.ui.lineEdit_promo.text().strip(), self.ui.lineEdit_num.text().strip()])
            self.data.commit()
        except Exception as e:
            if (i):
                display.refreshLabel(self.ui.label_res, "Les champs ne sont pas tous renseignés")
                i = 0
            else: display.refreshLabel(self.ui.label_res, "Impossible d'ajouter la représentation : " + repr(e))
        else:
            display.refreshLabel(self.ui.label_res, "Représentation ajoutée.")