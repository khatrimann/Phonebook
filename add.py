import os

import sys
from PyQt4 import QtGui, uic
from PyQt4.QtGui import *
import mysql.connector
import Database.main


path = os.getcwd()

qtCreatorFileADD = path + "/ADD.ui"  # Enter file here.

Ui_MainWindowADD, QtBaseClassADD = uic.loadUiType(qtCreatorFileADD)


class MyApp(QtGui.QMainWindow, Ui_MainWindowADD, QListWidget):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        Ui_MainWindowADD.__init__(self)
        QListWidget.__init__(self)
        QtGui.QListView.__init__(self)
        self.setupUi(self)
        # __metaclass__= Database.main
        self.add.clicked.connect(self.ADD)

        self.data = Database.main.MyApp
        try:
            self.cnx = mysql.connector.connect(user='root', password='toor',
                                               host='127.0.0.1',
                                               database='Phonebook')

            print("CONNECTED")

        except:
            print("BAD Connection")

        self.cursor = self.cnx.cursor()


    def ADD(self):
        print("ADDING DATA...")
        nameprefix = self.nameprefix.toPlainText()
        name = self.name.toPlainText()
        middlename = self.middlename.toPlainText()
        surname = self.surname.toPlainText()
        email = self.email.toPlainText()
        address = self.address.toPlainText()
        phone = self.phone.toPlainText()
        profilepath = QFileDialog.getOpenFileName(filter="*.jpg")
        print(profilepath)
        # self.profileset.setText(profilepath)
        profile = profilepath.split('/')
        print(profile[len(profile)-1])
        # os.system("cp "+profilepath+" "+path+"/ProfilePictures/"+profile[len(profile)-1])
        if nameprefix == "" or name =="" or surname == "" or email == "" or address == "" or phone == "":
            msg1 = QMessageBox()
            msg1.setIcon(QMessageBox.Warning)

            msg1.setText("One or more fields needs attention!!")
            msg1.setInformativeText("Fields unused")
            msg1.setWindowTitle("ERROR")
            # msg.setDetailedText("The details are as follows:\n\n" + string + " CANNOT BE NULL")
            msg1.exec_()
            print(name)
        else:
            try:
                query = "INSERT INTO info(Name_prefix,Middle_Name,Surname,Email,Address,Phone,First_Name, Profile) VALUES(\"" + nameprefix + "\", \"" + middlename + "\", \"" + surname + "\", \"" + email + "\", \"" + address + "\", " + phone +", \""+name+"\", \""+profile[len(profile)-1]+"\");"
                os.system("cp " + profilepath + " " + path + "/ProfilePictures/" + profile[len(profile) - 1])
                self.profileset.setText(profilepath)

                print(query)
                self.cursor.execute(query)
                self.cnx.commit()

                # self.cnx.close()
                # Database.main.MyApp.updatedata(self)
                msg2 = QMessageBox()
                msg2.setIcon(QMessageBox.Information)

                msg2.setText("Please Refresh!!")
                msg2.setWindowTitle("ATTENTION")
                # msg.setDetailedText("The details are as follows:\n\n" + string + " CANNOT BE NULL")
                msg2.exec_()
                # sys.exit()
            except:
                msg3 = QMessageBox()
                msg3.setIcon(QMessageBox.Warning)

                msg3.setText("One or more fields needs attention!!")
                msg3.setInformativeText("Error While Inserting")
                msg3.setWindowTitle("ERROR")
                msg3.setDetailedText("Phone number may already exist")
                msg3.exec_()

            sys.exit()

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
