import sqlite3
from utils import display
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import QDateTime
from PyQt5 import uic
from datetime import datetime
from time import strftime


class AppGestRes(QDialog):
    page_fin_dialog = None
    reponse = False
    add_doss_table = True
    CurrentDossier = 0
    select_ligne_date = False
    select_ligne_supp = False
    l_supp = []
    l_rang = []
    # Création d'un signal destiné à être émis lorsque la taFble est modifiée
    changedValue = pyqtSignal()

    def __init__(self, data: sqlite3.Connection):
        super(QDialog, self).__init__()
        self.ui = uic.loadUi("gui/Gest_Res.ui", self)
        self.data = data
        self.initComboBox()
        self.initTimeDate()
        self.ouvre_gest_res_window()

    ###VERIFICATION :
    def recup_donne(self):
        return int(self.CurrentRow.currentText().strip()), int(self.CurrentPlace.currentText().strip()) \
            , self.CurrentGender.currentText().strip(), datetime.now().strftime('%d-%m-%Y %H:%M:%S') \
            , self.ui.compte_dossier.value(), self.CurrentTimeEdit.text()

    def calcul_possible(self):
        # ICI SEUL LE CAS DU GENRE EST POSSIBLE, le choix des places et des rangs est obligé par l'appli quand on choisi une date.
        if not self.CurrentRow.currentText().strip():
            display.refreshLabel(self.ui.label_erreur_gest_res, "Choissisez une date valide")
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
        cursor.execute("SELECT dateRep FROM LesRepresentations")
        res = cursor.fetchall()
        for item in res:
            if item[0] == self.CurrentTimeEdit.text():
                if datetime.strptime(self.CurrentTimeEdit.text(), '%d/%m/%Y %H:%M') > datetime.now():
                    display.refreshLabel(self.ui.label_date_erreur, "Date correcte")
                    return True
                else:
                    display.refreshLabel(self.ui.label_date_erreur, "Représentation obsolète")
                    return False
            else:
                display.refreshLabel(self.ui.label_date_erreur, "Date incorrecte")
        return False

    def ajout_possible(self):
        if not self.calcul_possible() or not self.date_OK():
            return False
        return True

    def active_select_supp(self):
        self.l_supp = []
        self.select_ligne_supp = True
        self.selectedLines = sorted(
            set(
                index.row()
                for index in self.ui.table_currentDoss.selectionModel().selectedIndexes()
            )
        )
        for item in self.selectedLines:
            self.l_supp.append(self.ui.table_currentDoss.item(item, 0).text())

    def supp_liste_dossier(self):
        #EN FAISANT ça ON A UN PB SI PLUSIEURS PLACES ACHETEZ A LA MEME SECONDE, sleep() rajouter dans add_doss
        for k in self.l_supp:
            i = 0
            while i < (len(self.l)):
                if self.l[i][0] == int(k):
                    self.l.remove(self.l[i])
                    break
                i+=1

    def active_select_ligne_date(self):
        self.select_ligne_date = True
        self.Refresh_date()

    def Refresh_date(self):
        if self.select_ligne_date:
            self.selectedLine()
            self.select_ligne_date = False

    def fermer_OK(self):
        if self.table_doss(self.ui.compte_dossier.value()):
            display.refreshLabel(self.ui.label_erreur_gest_res, "Veuillez supprimez tous les tickets avant de fermer")
        else:
            self.close()

    ### INITIALISATION DE VALEURS
    def initTimeDate(self):
        datetime_object = str(datetime.now())
        date = datetime_object.split(" ")[0].split("-")
        time = datetime_object.split(" ")[1].split(":")
        self.CurrentTimeEdit.setDateTime(
            datetime(
                int(date[0]), int(date[1]), int(date[2]), int(time[0]), int(time[1])
            )
        )

    def initComboBox(self):
        cursor = self.data.cursor()
        cursor.execute("SELECT DISTINCT typePers FROM LesReductions ")
        res = cursor.fetchall()
        res.insert(0, ("",))
        for item in res:
            self.CurrentGender.addItem(item[0])

    def init_dossier_courant(self):
        cursor = self.data.cursor()
        cursor.execute("SELECT max(noDossier) FROM LesVentes")
        dernier_doss = cursor.fetchall()[0][0]
        if dernier_doss == None:  # PERMET DE GERER LE CAS OU IL Y A 0 Ventes la première fois
            self.CurrentDossier = 1
        else:
            self.CurrentDossier = dernier_doss + 1

    def init_list_rang(self):
        self.l_rang = []
        cursor = self.data.cursor()
        cursor.execute("SELECT DISTINCT noRang FROM LesPlaces ")
        res = cursor.fetchall()
        for item in res:
            self.l_rang.append(item[0])

    def init_prix_spec_promo_rep(self):
        cursor = self.data.cursor()
        cursor.execute("SELECT prixBaseSpec, promoRep FROM LesSpectacles "
                       "JOIN LesRepresentations USING(noSpec) WHERE dateRep = ? ",
                       [self.CurrentTimeEdit.text()])
        prix_spec_et_promo_rep = cursor.fetchall()
        return prix_spec_et_promo_rep[0][0], (prix_spec_et_promo_rep[0][1])



    def init_tarif_reduit_taux_zone(self):
        cursor = self.data.cursor()
        cursor.execute(
            "SELECT tarifReduit FROM LesReductions WHERE typePers = ? ",
            [self.CurrentGender.currentText().strip()])
        res = cursor.fetchall()
        tarif_reduit = res[0][0]
        if int(self.CurrentRow.currentText().strip()) == 3:
            return 1.5, tarif_reduit
        elif int(self.CurrentRow.currentText().strip()) == 4:
            return 2, tarif_reduit
        else:
            return 1, tarif_reduit


    def renvoi_prix_dossier(self):
        cursor = self.data.cursor()
        cursor.execute("SELECT prixDossier FROM [LesDossiers] WHERE noDossier = ?", [(self.CurrentDossier)])
        res = cursor.fetchall()
        if res:
            return round(res[0][0], 2)
        else: return 0

    def update_date_transac(self):
        cursor = self.data.cursor()
        cursor.execute("UPDATE LesTickets SET dateTrans = ? WHERE noDossier = ?",
                       [datetime.now().strftime('%d-%m-%Y %H:%M:%S'), (self.CurrentDossier)])
        self.data.commit()
        self.changedValue.emit()

    def doss_exist(self):
        cursor = self.data.cursor()
        try:
            cursor.execute("INSERT INTO NumeroDossier DEFAULT VALUES")
        except Exception as e:
            display.refreshLabel(self.ui.label_erreur_gest_res, "")
        else:
            self.data.commit()
            self.changedValue.emit()

    def selectedLine(self):
        # display.refreshLabel(self.ui.label_erreur_gest_res, "")
        self.selectedLines = sorted(
            set(
                index.row()
                for index in self.ui.tableGestRes.selectionModel().selectedIndexes()
            )
        )

        self.selectedDate = self.ui.tableGestRes.item(self.selectedLines[0], 1).text()
        try:
            timedate = self.selectedDate.split(" ")
            date = timedate[0].split("/")
            time = timedate[1].split(":")
            self.CurrentTimeEdit.setDateTime(
                datetime(
                    int(date[2]), int(date[1]), int(date[0]), int(time[0]), int(time[1])
                )
            )
        except Exception as e:
            display.refreshLabel(self.ui.label_table_erreur, "Impossible de sélectionner cette représentation")
        else:
            display.refreshLabel(self.ui.label_table_erreur, "")

    # FONCTION PERMETTANT DE LE FONCTIONNEMENT DE L'APPLICATION

    def ouvre_gest_res_window(self):
        self.l = []
        self.init_dossier_courant()
        self.compte_dossier.setValue(self.CurrentDossier)
        self.prix_total_doss.setValue(0)
        self.fenetre_representation()

    def fenetre_representation(self):
        display.refreshLabel(self.ui.label_table_erreur, "")
        try:
            cursor = self.data.cursor()
            result = cursor.execute(
                "SELECT nomSpec, DateRep, nbPlaceDisponibles FROM Salle WHERE dateRep IS NOT NULL")
        except Exception as e:
            self.ui.tableGestRes.setRowCount(0)
            display.refreshLabel(self.ui.label_table_erreur,
                                 "Impossible d'afficher les résultats : " + repr(e), )
        else:
            # Remplir la table de gauche avec les représentaions:
            i = display.refreshGenericData(self.ui.tableGestRes, result)
            if i == 0:
                display.refreshLabel(self.ui.label_table_erreur, "Aucune représentation n'est programmé")

    def refreshnbRang(self):
        self.CurrentRow.clear()
        self.init_list_rang()
        cursor = self.data.cursor()
        cursor.execute("SELECT DISTINCT noRang FROM LesTickets "
                       "GROUP BY noRang, dateRep HAVING dateRep = ? and (5 - count(noPlace)) = 0 ",
                       [self.CurrentTimeEdit.text()])
        res = cursor.fetchall()
        for item in res:
            self.l_rang.remove(item[0])
        for item in self.l_rang:
            self.CurrentRow.addItem(str(item))
        self.l_rang = []

    def refreshnbPlace(self):
        self.CurrentPlace.clear()
        cursor = self.data.cursor()
        cursor.execute("SELECT noPlace FROM LesPlaces WHERE noRang = ? "
                       "and noPlace not in (SELECT noPlace FROM LesVentes "
                       "WHERE noRang = ? and dateRep = ?)",
                       [self.ui.CurrentRow.currentText().strip(),
                        self.ui.CurrentRow.currentText().strip(), self.CurrentTimeEdit.text()])
        res = cursor.fetchall()
        if res == []:
            display.refreshLabel(self.ui.label_rang_erreur, "Rang complet ou indisponible")
        else:
            display.refreshLabel(self.ui.label_rang_erreur, "")
            for item in res:
                self.CurrentPlace.addItem(str(item[0]))

    def table_doss(self, numDoss):
        cursor = self.data.cursor()
        result = cursor.execute("SELECT noTrans, dateRep, noRang, noPlace, typePers "
                                "FROM LesVentes WHERE noDossier = %d" %numDoss)
        i = display.refreshGenericData(self.ui.table_currentDoss, result)
        self.prix_total_doss.setValue(self.renvoi_prix_dossier())
        if i == 0:
            self.l = []
            display.refreshLabel(self.ui.label_erreur_gest_res, "")
            return False
        else:
            return True

    def calcul_prix(self):
        cursor = self.data.cursor()
        if self.calcul_possible():
            if self.date_OK():
                prixbaserep, promo_rep = self.init_prix_spec_promo_rep()
                tauxZone, tarif_reduit = self.init_tarif_reduit_taux_zone()
                self.init_tarif_reduit_taux_zone()
                prix = prixbaserep * (1 - promo_rep) * (1 - tarif_reduit) * tauxZone
                self.CurrentPrice.setValue(float(prix))
        else:
            self.CurrentPrice.setValue(float(0))

     #AJOUT/SUPPRESSION/CONFIRMATION

    def add_doss(self):
        cursor = self.data.cursor()
        if not self.ajout_possible():
            display.refreshLabel(self.ui.label_erreur_gest_res, "Veuillez remplir tous les champs correctement")
            return
        noRang, noPlace, typePers, datePreTrans, numDossier, dateRep = self.recup_donne()
        try:
            self.doss_exist()
            cursor.execute("INSERT INTO LesTickets (dateTrans, noPlace, noRang, typePers, noDossier, dateRep)"
                           "VALUES (?, ?, ?, ?, ?, ?)",
                           [datePreTrans, noPlace, noRang, typePers, numDossier, dateRep])
        except Exception as e:
            display.refreshLabel(self.ui.label_erreur_gest_res, "Impossible d'achetez ce ticket: " + repr(e))
            return
        else:
            self.data.commit()
            self.changedValue.emit()
            cursor.execute("SELECT noTrans FROM LesTickets WHERE dateTrans = ?", [datePreTrans])
            res = cursor.fetchall()
            self.l.append((res[0][0],datePreTrans, noPlace, noRang, typePers, numDossier, dateRep))
            self.refreshnbRang()
            self.fenetre_representation()
            self.table_doss(numDossier)


    def supp_doss(self):
        cursor = self.data.cursor()
        if self.select_ligne_supp :
            self.select_ligne_supp = False
            try:
                for item in self.l_supp:
                    cursor.execute("DELETE FROM LesTickets "
                               "WHERE noTrans = ?", [item])
            except Exception as e:
                display.refreshLabel(self.ui.label_erreur_gest_res, "Impossible de supprimer " + repr(e))
            else:
                self.supp_liste_dossier()
                self.data.commit()
                self.changedValue.emit()
                self.fenetre_representation()
                self.refreshnbRang()
                self.table_doss(self.ui.compte_dossier.value())
        else:
            if self.l:
                display.refreshLabel(self.ui.label_erreur_gest_res, "Selectionnez un ticket a supprimer. ")
            else:
                display.refreshLabel(self.ui.label_erreur_gest_res, "Ajoutez dabord un ticket. ")

    def all_supp(self):
        cursor = self.data.cursor()
        try:
            cursor.execute("SELECT nbTicket FROM [LesDossiers] "
                           "WHERE noDossier = ?", [self.ui.compte_dossier.value()])
            nbTicket = cursor.fetchall()[0][0]
        except Exception as e:
            display.refreshLabel(self.ui.label_erreur_gest_res, "Rien a supprimer ")
        else:
            for i in range(nbTicket):
                cursor.execute("DELETE FROM LesTickets "
                           "WHERE noDossier = ? ", [self.ui.compte_dossier.value()])
            self.data.commit()
            self.changedValue.emit()
            self.fenetre_representation()
            self.refreshnbRang()
            self.table_doss(self.ui.compte_dossier.value())


    def confirmez_payez(self):
        if self.l:
            try:
                cursor = self.data.cursor()
                cursor.execute("SELECT prixDossier FROM [LesDossiers] WHERE noDossier = ?", [(self.CurrentDossier)])
            except Exception as e:
                display.refreshLabel(
                    self.ui.label_erreur_gest_res,"Impossible de créer ce dossier : " + repr(e))
            else:
                self.update_date_transac()
                self.l = []
                self.table_doss(self.ui.compte_dossier.value()+ 1)
                self.ouvre_gest_res_window()
        else:
            display.refreshLabel(
                self.ui.label_erreur_gest_res,"Achetez au moins une place.")