import sqlite3
from utils import display
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import QDateTime
import datetime
from PyQt5 import uic


class AppGestRes(QDialog):

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
        try:
            cursor = self.data.cursor()
            result = cursor.execute(
                "SELECT nomSpec, DateRep, nbPlaceDisponibles \
              FROM Salle"
            )
        except Exception as e:
            self.ui.tableGestRes.setRowCount(0)
            display.refreshLabel(
                self.ui.label_table_erreur,
                "Impossible d'afficher les résultats : " + repr(e),
            )
        else:
            i = display.refreshGenericData(self.ui.tableGestRes, result)
            self.initComboBox()
            if i == 0:
                display.refreshLabel(
                    self.ui.label_table_erreur, "Aucune représentation n'est programmé"
                )

    # initialisation du menu deroulant
    def initComboBox(self):
        self.GenderList = []
        self.PlaceList = []
        self.RowList = []
        cursor = self.data.cursor()
        # Pour le genre :
        cursor.execute("SELECT DISTINCT typePers FROM LesReductions ")
        res = cursor.fetchall()
        res.insert(0, ("",))
        for item in res:
            self.GenderList.append(item[0])
            self.CurrentGender.addItem(item[0])

    def selectedLine(self):
        self.selectedLines = sorted(
            set(
                index.row()
                for index in self.ui.tableGestRes.selectionModel().selectedIndexes()
            )
        )
        # self.selectedNom = self.ui.tableGestRep.item(self.selectedLines[0], 0).text()
        self.selectedDate = self.ui.tableGestRes.item(self.selectedLines[0], 1).text()
        timedate = self.selectedDate.split(" ")
        date = timedate[0].split("/")
        time = timedate[1].split(":")
        self.CurrentTimeEdit.setDateTime(
            datetime.datetime(
                int(date[2]), int(date[1]), int(date[0]), int(time[0]), int(time[1])
            )
        )

    def refreshnbRang(self):
        l_tout_rang = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
        cursor = self.data.cursor()
        cursor.execute("SELECT DISTINCT noRang FROM LesVentes "
                        "GROUP BY noRang, dateRep HAVING dateRep = ? and (25 - count(noPlace)) = 0 ", [self.CurrentTimeEdit.text()])
        res = cursor.fetchall()
        for item in res:
            l_tout_rang.remove(item[0])
        self.CurrentRow.clear();
        for item in l_tout_rang:
            self.RowList.append(item)
            self.CurrentRow.addItem(str(item))

    def refreshnbPlace(self):
        self.CurrentPlace.clear();
        cursor = self.data.cursor()
        cursor.execute("SELECT noPlace FROM LesPlaces WHERE noRang = ? "
                       "and noPlace not in (SELECT noPlace FROM LesVentes "
                        "WHERE noRang = ? and dateRep = ?)",
                       [self.ui.CurrentRow.currentText().strip(),
                        self.ui.CurrentRow.currentText().strip(),self.CurrentTimeEdit.text()])
        res = cursor.fetchall()
        for item in res:
            self.PlaceList.append(str(item[0]))
            self.CurrentPlace.addItem(str(item[0]))
        # self.calcul_prix()

    def calcul_prix(self):
        cursor = self.data.cursor()
        cursor.execute("SELECT prixBaseSpec, promoRep FROM LesSpectacles JOIN LesRepresentations USING(noSpec) WHERE dateRep = ? ",
                       [self.CurrentTimeEdit.text()])
        prix_spec_et_promo_rep = cursor.fetchall()
        if not prix_spec_et_promo_rep:
            return
        prixBaseRep = prix_spec_et_promo_rep[0][0]
        promo_rep = (prix_spec_et_promo_rep[0][1])

        # rang <= 4 -> orchestre donc *1,5
        # rang >= 16 balcon donc *2
        print("yo", self.CurrentRow.currentText().strip())
        if not self.CurrentRow.currentText().strip() :
            return
        if int(self.CurrentRow.currentText().strip()) <= 4:
            tauxZone = 1.5
        elif int(self.CurrentRow.currentText().strip()) >= 16:
            tauxZone = 2
        else:
            tauxZone = 1

        cursor.execute(
            "SELECT tarifReduit FROM LesReductions WHERE typePers = ? ",
            [self.CurrentGender.currentText().strip()])
        tarif_reduit = cursor.fetchall()
        if not tarif_reduit:
            return
        prix = prixBaseRep * (1-promo_rep) * (1-tarif_reduit[0][0]) * tauxZone
        self.CurrentPrice.setValue(float(prix))


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
