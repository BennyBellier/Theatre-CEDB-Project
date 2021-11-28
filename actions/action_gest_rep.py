
import sqlite3
from utils import display
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import pyqtSignal
from PyQt5 import uic
from actions.action_gest_rep_add import AppGestRep_add


class AppGestRep(QDialog):

    gest_rep_add_dialog = None  # Fenetre d'ajout de representation

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

    def add_rep(self):
      if self.gest_rep_add_dialog is not None:
            self.gest_rep_add_dialog.close()
      self.gest_rep_add_dialog = AppGestRep_add(self.data)
      self.gest_rep_add_dialog.show()
      # self.changedValue.connect()

    def closeEvent(self, event):

          # On ferme les éventuelles fenêtres encore ouvertes
          if (self.gest_rep_add_dialog is not None):
              self.gest_rep_add_dialog.close()

          # On laisse l'évènement de clôture se terminer normalement
          event.accept()

    def modif_rep():
        print("0")

    def delete_rep():
        print("0")