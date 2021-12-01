import sqlite3
from utils import display
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import QDateTime
import datetime
from PyQt5 import uic
from datetime import datetime
from time import strftime


class AppGestRes(QDialog):
    page_fin_dialog = None
    reponse = False
    add_doss_table = True
    CurrentDossier = 0
    select_ligne = False

    # Création d'un signal destiné à être émis lorsque la taFble est modifiée
    changedValue = pyqtSignal()

    def __init__(self, data: sqlite3.Connection):
        super(QDialog, self).__init__()
        self.ui = uic.loadUi("gui/Gest_Res.ui", self)
        self.data = data
        self.initComboBox()
        self.ouvre_gest_res_window()

    def initComboBox(self):
        cursor = self.data.cursor()
        cursor.execute("SELECT DISTINCT typePers FROM LesReductions ")
        res = cursor.fetchall()
        res.insert(0, ("",))
        for item in res:
            self.CurrentGender.addItem(item[0])

    def ouvre_gest_res_window(self):
        self.l = []
        # Initialise le compteur avec le dossier suivant:
        self.get_current_dossier()
        self.compte_dossier.setValue(self.CurrentDossier)
        self.fenetre_representation()

        # self.refreshResult()

    def fenetre_representation(self):
        display.refreshLabel(self.ui.label_table_erreur, "")
        try:
            cursor = self.data.cursor()
            result = cursor.execute(
                "SELECT nomSpec, DateRep, nbPlaceDisponibles FROM Salle")
        except Exception as e:
            self.ui.tableGestRes.setRowCount(0)
            display.refreshLabel(self.ui.label_table_erreur,
                "Impossible d'afficher les résultats : " + repr(e),)
        else:
            #Remplir la table de gauche avec les représentaions:
            i = display.refreshGenericData(self.ui.tableGestRes, result)
            if i == 0:
                display.refreshLabel(self.ui.label_table_erreur, "Aucune représentation n'est programmé")

    def get_current_dossier(self):
        cursor = self.data.cursor()
        cursor.execute("SELECT max(noDossier) FROM LesVentes")
        dernier_doss = cursor.fetchall()[0][0]
        if dernier_doss == None: #PERMET DE GERER LE CAS OU IL Y A 0 Ventes la première fois
            self.CurrentDossier = 1
        else:
            self.CurrentDossier = dernier_doss + 1
        # print(self.CurrentDossier)

    # Fonction potentiellement inutile mais permet de mieux comprendre
    def active_select_ligne(self):
        self.select_ligne = True
        self.Refresh_date()

    def Refresh_date(self):
        if self.select_ligne:
            self.selectedLine()
            self.select_ligne = False

    def selectedLine(self):
        # display.refreshLabel(self.ui.label_erreur_gest_res, "")
        self.selectedLines = sorted(
            set(
                index.row()
                for index in self.ui.tableGestRes.selectionModel().selectedIndexes()
            )
        )
        self.selectedDate = self.ui.tableGestRes.item(self.selectedLines[0], 1).text()
        timedate = self.selectedDate.split(" ")
        date = timedate[0].split("/")
        time = timedate[1].split(":")
        self.CurrentTimeEdit.setDateTime(
            datetime(
                int(date[2]), int(date[1]), int(date[0]), int(time[0]), int(time[1])
            )
        )
    def refreshnbRang(self):
        # display.refreshLabel(self.ui.label_erreur_gest_res, "")
        self.CurrentRow.clear()
        cursor = self.data.cursor()
        l_tout_rang = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]

        cursor.execute("SELECT DISTINCT noRang FROM LesVentes "
                        "GROUP BY noRang, dateRep HAVING dateRep = ? and (25 - count(noPlace)) = 0 ", [self.CurrentTimeEdit.text()])
        res = cursor.fetchall()
        for item in res:
            l_tout_rang.remove(item[0])

        for item in l_tout_rang:
            self.CurrentRow.addItem(str(item))
        # self.refreshnbPlace()

    def refreshnbPlace(self):
        self.CurrentPlace.clear()
        cursor = self.data.cursor()
        cursor.execute("SELECT noPlace FROM LesPlaces WHERE noRang = ? "
                       "and noPlace not in (SELECT noPlace FROM LesVentes "
                        "WHERE noRang = ? and dateRep = ?)",
                       [self.ui.CurrentRow.currentText().strip(),
                        self.ui.CurrentRow.currentText().strip(),self.CurrentTimeEdit.text()])
        res = cursor.fetchall()
        for item in res:
            self.CurrentPlace.addItem(str(item[0]))

    def calcul_possible(self):
        # ICI SEUL LE CAS DU GENRE EST POSSIBLE, le choix des places et des rangs est obligé par l'appli quand on choisi une date.
        if not self.CurrentRow.currentText().strip():
            display.refreshLabel(self.ui.label_erreur_gest_res, "Choissisez un rang")
        elif not self.CurrentPlace.currentText().strip():
            display.refreshLabel(self.ui.label_erreur_gest_res, "Choissisez une place")
        elif not self.CurrentGender.currentText().strip():
            display.refreshLabel(self.ui.label_erreur_gest_res, "Choissisez un genre")
        else:
            display.refreshLabel(self.ui.label_erreur_gest_res, "")
            display.refreshLabel(self.ui.label_erreur_gest_res, "")
            display.refreshLabel(self.ui.label_erreur_gest_res, "")
            return True
        return False

    def date_OK(self):
        cursor = self.data.cursor()
        cursor.execute("SELECT dateRep FROM LesRepresentations ")
        res = cursor.fetchall()
        for item in res:
            if item[0] == self.CurrentTimeEdit.text():
                display.refreshLabel(self.ui.label_date_erreur, "Date correcte")
                return True
            else:
                display.refreshLabel(self.ui.label_date_erreur, "Date incorrecte")
        return False

    def calcul_prix(self):
        cursor = self.data.cursor()
        if self.calcul_possible():
            if self.date_OK():
                cursor.execute("SELECT prixBaseSpec, promoRep FROM LesSpectacles JOIN LesRepresentations USING(noSpec) WHERE dateRep = ? ",
                               [self.CurrentTimeEdit.text()])
                prix_spec_et_promo_rep = cursor.fetchall()
                if not prix_spec_et_promo_rep:
                    return
                prixBaseRep = prix_spec_et_promo_rep[0][0]
                promo_rep = (prix_spec_et_promo_rep[0][1])
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
        else:
            self.CurrentPrice.setValue(float(0))

    def ajout_possible(self):
        if not self.calcul_possible() or not self.date_OK():
            return False
        return True

    def doss_exist(self, numDossier):
        cursor = self.data.cursor()
        try:
            cursor.execute("INSERT INTO NumeroDossier (noDossier) VALUES (?)", [numDossier])
        except Exception as e:
            display.refreshLabel(self.ui.label_erreur_gest_res,"")
        else:
            self.data.commit()
            self.changedValue.emit()


    def add_doss(self):
        cursor = self.data.cursor()
        if not self.ajout_possible():
            display.refreshLabel(self.ui.label_erreur_gest_res,"Veuillez remplir tous les champs correctement")
            return

        dateRep = self.CurrentTimeEdit.text()
        noRang = int(self.CurrentRow.currentText().strip())
        noPlace = int(self.CurrentPlace.currentText().strip())
        typePers = self.CurrentGender.currentText().strip()
        PrixPlace = self.ui.CurrentPrice.value()
        datePreTrans = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
        numDossier = self.ui.compte_dossier.value()
        #PEUT ETRE INUTILE
        # l_doss = []
        # l_doss.append((datePreTrans, PrixPlace, noPlace, noRang, typePers, numDossier, dateRep))
        # print(l_doss)
        try:
            self.doss_exist(numDossier)
            cursor.execute("INSERT INTO LesVentes (dateTrans, prixTotal, noPlace, noRang, typePers, noDossier, dateRep)"
                           "VALUES (?, ?, ?, ?, ?, ?, ?)",
                           [datePreTrans, PrixPlace, noPlace, noRang, typePers, numDossier, dateRep])
        except Exception as e:
            display.refreshLabel(self.ui.label_erreur_gest_res,"Impossible d'achetez ce ticket. ")
            print(repr(e)) #ICII a supprimer plus tard
            return
        else:
            self.data.commit()
            self.changedValue.emit()
            self.l.append((datePreTrans, PrixPlace, noPlace, noRang, typePers, numDossier, dateRep))
            # print(self.l)
            result = cursor.execute("SELECT noTrans, noRang, noPlace, typePers "
                                    "FROM LesVentes WHERE noDossier = ?",
                                    [numDossier])
            i = display.refreshGenericData(self.ui.table_currentDoss, result)
            if i == 0:
                display.refreshLabel(self.ui.erreur_gest_res, "Aucun ajout dans le dossier")
            self.refreshnbRang()
            #RAFRAICHIR A GAUCHE :
            self.fenetre_representation()

    def confirmez_payez(self):
        #print(self.ui.compte_dossier.value()) == print(self.CurrentDossier) C'est vrai
        #print(self.l)
        if self.l:
            try:
                cursor = self.data.cursor()
                cursor.execute("SELECT prixDossier FROM [LesDossiers] WHERE noDossier = ?", [(self.CurrentDossier)])
                res = cursor.fetchall()
            except Exception as e:
                display.refreshLabel(
                    self.ui.label_erreur_gest_res,
                    "Impossible de créer ce dossier : " + repr(e),
                )
            else:
                print("Vous devez payez : ?", round(res[0][0],2))
                self.l = []
                self.ui.table_currentDoss.clear()
                self.ouvre_gest_res_window()
        else:
            display.refreshLabel(
                self.ui.label_erreur_gest_res,
                "Achetez au moins une place ")


    # def incremente_dossier(self):
    #     self.get_current_dossier()
    #     if not self.reponse:
    #         # numDossier = self.CurrentDossier
    #         self.reponse = True
    #     else:
    #         self.CurrentDossier -= 1


#
# #     #################################################################################################
# #
#     def confirmez_payez(self):
#         # print(self.ui.compte_dossier.value()) == print(self.CurrentDossier) C'est vrai
#         print(self.l)
#         if self.l:
#             try:
#                 cursor = self.data.cursor()
#
#                 cursor.execute("SELECT prixDossier FROM [LesDossiers] WHERE noDossier = ?", [(self.CurrentDossier)])
#                 res = cursor.fetchall()
#
#             except Exception as e:
#                 display.refreshLabel(
#                     self.ui.label_erreur_gest_res,
#                     "Impossible de créer ce dossier : " + repr(e),
#                 )
#             else:
#                 self.ouvrir_msg_fin()
#         else:
#             display.refreshLabel(
#                 self.ui.label_erreur_gest_res,
#                 "Achetez au moins une place ")
#
#     def ouvrir_msg_fin(self):
#         if self.page_fin_dialog is not None:
#             self.page_fin_dialog.close()
#         self.page_fin_dialog = App_Msg_fin(self.data, self.CurrentDossier)
#         self.page_fin_dialog.show()
#
#     def closeEvent(self, event):
#
#         # On ferme les éventuelles fenêtres encore ouvertes
#         if self.page_fin_dialog is not None:
#             self.page_fin_dialog.close()
#         # On laisse l'évènement de clôture se terminer normalement
#         event.accept()
#
# class App_Msg_fin(QDialog):
#
#     def __init__(self, data:sqlite3.Connection, CurrentDossier):
#         super(QDialog, self).__init__()
#         self.ui = uic.loadUi("gui/Gest_Res_fin.ui", self)
#         self.spinBox.setValue(CurrentDossier)
#         self.data = data


    # def maj_view(self):
    #     cursor = self.data.cursor()
    #     cursor.execute("DROP VIEW IF EXISTS [LesDossiers]")
    #     cursor.execute(
    #         "CREATE VIEW [LesDossiers] AS "
    #         "select noDossier, sum(prixTotal) as prixDossier "
    #         "from NumeroDossier join LesVentes using (noDossier) "
    #         "GROUP BY noDossier"
    #     )
    #     self.data.commit()

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
