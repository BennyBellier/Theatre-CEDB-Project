
import sqlite3
from utils import display
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSlot
from PyQt5 import uic

class AppGestRep(QDialog):

  def __init__(self, data:sqlite3.Connection):
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
                FROM LesSpectacles JOIN LesRepresentations USING (noSpec)")
      except Exception as e:
          self.ui.tableRepVide.setRowCount(0)
          display.refreshLabel(self.ui.label_gest_rep, "Impossible d'afficher les résultats : " + repr(e))
      else:
          i = display.refreshGenericData(self.ui.tableGestRep, result)
          if i == 0:
              display.refreshLabel(self.ui.label_gest_rep, "Aucun résultat")

  def add_rep():
    print("0")

  def modif_rep():
    print("0")

  def delete_rep():
    print("0")