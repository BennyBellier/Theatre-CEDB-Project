import sqlite3
from utils import display
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import QDateTime
import datetime
from PyQt5 import uic


class AppGestRes(QDialog):
    """
    Fenêtre de gestion des représentations : ajout, modification, suppression
    """

    # on prévoit les variables pour acceuillir les fenetres supplementaires
    # fct_verif_supp_dialog = None

    # valeur pour effectuer le Ctrl + z
    # ancientNom = ""
    # ancientDate = ""
    # ancientPrix = 0
    # ancientPromo = 0
    #
    # # booleen si on ne veut plus afficher la fenêtre de prevention avant suppression
    # prevent_delete = 1

    def __init__(self, data: sqlite3.Connection):
        super(QDialog, self).__init__()
        self.ui = uic.loadUi("gui/Gest_Res.ui", self)
        self.data = data
        self.refreshResult()

    # Fonction de mise à joru de l'affichage
    @pyqtSlot()
    def refreshResult(self):
        display.refreshLabel(self.ui.label_table_erreur, "")
        display.refreshLabel(self.ui.label_erreur_gest_res, "")
        # try:
        #     cursor = self.data.cursor()
        #     result = cursor.execute(
        #         "SELECT nomSpec, DateRep, PrixBaseSpec, promoRep \
        #       FROM LesSpectacles JOIN LesRepresentations USING (noSpec)"
        #     )
        # except Exception as e:
        #     self.ui.tableGestRep.setRowCount(0)
        #     display.refreshLabel(
        #         self.ui.label_table,
        #         "Impossible d'afficher les résultats : " + repr(e),
        #     )
        # else:
        #     i = display.refreshGenericData(self.ui.tableGestRep, result)
        #     self.initComboBox()
        #     if i == 0:
        #         display.refreshLabel(
        #             self.ui.label_table, "Aucun représentation n'est programmé"
        #         )

    # initialisation du menu deroulant
#     def initComboBox(self):
#         self.NameList = []
#         cursor = self.data.cursor()
#         cursor.execute("SELECT DISTINCT nomSpec FROM LesSpectacles")
#         res = cursor.fetchall()
#         res.insert(0, ("",))
#         for item in res:
#             self.NameList.append(item[0])
#             self.CurrentName.addItem(item[0])
#
#     # lorsque qu'une case est selectionner alors on recupere les elements de la ligne
#     def selectedLine(self):
#         self.selectedLines = sorted(
#             set(
#                 index.row()
#                 for index in self.ui.tableGestRep.selectionModel().selectedIndexes()
#             )
#         )
#         self.selectedNom = self.ui.tableGestRep.item(self.selectedLines[0], 0).text()
#         self.selectedDate = self.ui.tableGestRep.item(self.selectedLines[0], 1).text()
#         self.selectedPrix = self.ui.tableGestRep.item(self.selectedLines[0], 2).text()
#         self.selectedPromo = self.ui.tableGestRep.item(self.selectedLines[0], 3).text()
#         self.refreshModif()
#
#     def refreshModif(self):
#         self.CurrentName.setCurrentIndex(self.NameList.index(self.selectedNom))
#         timedate = self.selectedDate.split(" ")
#         date = timedate[0].split("/")
#         time = timedate[1].split(":")
#         self.CurrentTimeEdit.setDateTime(
#             datetime.datetime(
#                 int(date[2]), int(date[1]), int(date[0]), int(time[0]), int(time[1])
#             )
#         )
#         self.CurrentPrice.setValue(float(self.selectedPrix))
#         self.CurrentPromotion.setValue(float(self.selectedPromo))
#
#     #################################################################################################
#     # gestion des bouton
#     #################################################################################################
#
#     # en cas de clic sur le bouton ajouter
#     def addRep(self):
#         pass
#
#     # en cas de clic sur le bouton modifier
#     def modifRep(self):
#         pass
#
#     # en cas de clic sur le bouton supprimer
#     def deleteRep(self):
#         display.refreshLabel(self.ui.label_modif, "")
#         if self.selectedLines == None:
#             display.refreshLabel(
#                 self.ui.label_modif,
#                 "Veuillez selectionner une ou plusieurs ligne(s) à supprimer !",
#             )
#         else:
#             print(self.selectedLines)
#             for row in self.selectedLines:
#                 cursor = self.data.cursor()
#                 cursor.execute(
#                     "SELECT noSpec FROM LesSpectacles WHERE nomSpec = ?",
#                     (self.ui.tableGestRep.item(row, 0).text(),),
#                 )
#                 delete_number = cursor.fetchall()
#                 if self.prevent_delete:
#                     self.openVerifSupp(
#                         delete_number[0][0],
#                         self.ui.tableGestRep.item(row, 1).text(),
#                         self.ui.tableGestRep.item(row, 3).text(),
#                     )
#                 result = cursor.execute(
#                     "DELETE FROM LesRepresentations WHERE noSpec = ? and dateRep = ? and promorep = ?",
#                     [
#                         delete_number[0][0],
#                         self.ui.tableGestRep.item(row, 1).text(),
#                         self.ui.tableGestRep.item(row, 3).text(),
#                     ],
#                 )
#             self.data.commit()
#             self.refreshResult()
#
#     def openVerifSupp(self, nomSpec, dateRep, promo):
#         if self.fct_verif_supp_dialog is not None:
#             self.fct_verif_supp_dialog.close()
#         self.fct_verif_supp_dialog = AppVerifSupp(nomSpec, dateRep, promo)
#         self.response, self.prevent_delete = AppVerifSupp().value()
#         print(prevent_delete)
#         self.fct_verif_supp_dialog.show()
#
#     # en cas d'appuie sur les toucher Ctrl + z
#     def CtrlZ(self):
#         pass
#
#     #################################################################################################
#     # Cloture des fenetres
#     #################################################################################################
#
#     def closeEvent(self, event):
#
#         # On ferme les éventuelles fenêtres encore ouvertes
#         if self.fct_verif_supp_dialog is not None:
#             self.fct_verif_supp_dialog.close()
#
#         # On laisse l'évènement de clôture se terminer normalement
#         event.accept()
#
#
# class AppVerifSupp(AppGestRep):
#     """
#     Fenêtre d'avertissement avant suppression
#     """
#
#     response = 0
#     prevent_delete = 1
#
#     def __init__(self, nomSpec, dateRep, promo):
#         self.ui = uic.loadUI("gui/dialogue_verif.ui", self)
#         display.refreshLabel(self.ui.label_nomRep, nomSpec)
#         display.refreshLabel(
#             self.ui.label_dateRep, "Date de la Représentation : " + dateRep
#         )
#         display.refreshLabel(
#             self.ui.label_promoRep, "Promotion de la représentation : " + promo
#         )
#
#     def value(self):
#         return self.response, self.prevent_delete
#
#     def delete(self):
#         self.response = 1
#
#     def always_delete(self):
#         self.prevent_delete = 0