
import sqlite3
from utils import display
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSlot
from PyQt5 import uic

# Classe permettant d'afficher la fenêtre de visualisation des données
class AppTablesDataV1(QDialog):

    # Constructeur
    def __init__(self, data:sqlite3.Connection):
        super(QDialog, self).__init__()
        self.ui = uic.loadUi("gui/v1_tablesData.ui", self)
        self.data = data

        # On met à jour l'affichage avec les données actuellement présentes dans la base
        self.refreshAllTablesV1()

    ####################################################################################################################
    # Méthodes permettant de rafraichir les différentes tables
    ####################################################################################################################

    # Fonction de mise à jour de l'affichage d'une seule table
    def refreshTable(self, label, table, query):
        display.refreshLabel(label, "")
        try:
            cursor = self.data.cursor()
            result = cursor.execute(query)
        except Exception as e:
            table.setRowCount(0)
            display.refreshLabel(label, "Impossible d'afficher les données de la table : " + repr(e))
        else:
            display.refreshGenericData(table, result)


    # Fonction permettant de mettre à jour toutes les tables
    @pyqtSlot()
    def refreshAllTablesV1(self):

        # TODOFAIS 1.3 : modifier pour afficher les nouveaux éléments (il faut aussi changer le fichier .ui correspondant)
        # TODOFAIS 1.4 : modifier pour afficher les nouveaux éléments (il faut aussi changer le fichier .ui correspondant)
        # TODOFAIS 1.5 : modifier pour afficher les nouveaux éléments (il faut aussi changer le fichier .ui correspondant)
        self.refreshTable(self.ui.label_representations, self.ui.tableSpectacles,
                          "SELECT noSpec, nomSpec, prixBaseSpec "
                          "FROM LesSpectacles")
        self.refreshTable(self.ui.label_representations, self.ui.tableRepresentations,
                          "SELECT dateRep, promoRep , noSpec "
                          "FROM LesRepresentations")
        self.refreshTable(self.ui.label_places, self.ui.tablePlaces,
                          "SELECT noPlace, noRang, noZone "
                          "FROM LesPlaces")
        self.refreshTable(self.ui.label_places, self.ui.tableZones,
                          "SELECT noZone, catZone "
                          "FROM LesZones")
        self.refreshTable(self.ui.label_places, self.ui.tableTypeZones,
                          "SELECT catZone, tauxZone "
                          "FROM TypeZones")
        self.refreshTable(self.ui.label_places, self.ui.tableReductions,
                          "SELECT typePers, tarifReduit "
                          "FROM LesReductions")