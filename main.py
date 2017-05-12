import os
import sys

import mysql.connector
from PyQt4 import QtGui, uic
from PyQt4.QtGui import *

# QListWidget, QListWidgetItem, QListView

path = os.getcwd()

qtCreatorFile = path + "/maindb.ui"  # Enter file here.

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)


# qtCreatorFileADD = path + "/ADD.ui"  # Enter file here.
#
# Ui_MainWindowADD, QtBaseClassADD = uic.loadUiType(qtCreatorFileADD)
#
#
# class MyAppADD(QtGui.QDialog,QtGui.QMainWindow, Ui_MainWindowADD):
#     def __init__(self, parent=None):
#         super(MyAppADD,self).__init__(parent)
#         QtGui.QMainWindow.__init__(self)
#         Ui_MainWindowADD.__init__(self)
#         # QListWidget.__init__(self)
#         # QtGui.QListView.__init__(self)
#         self.setupUi(self)
#
#         self.add.clicked.connect(self.ADD)
#
#
#         try:
#             self.cnx = mysql.connector.connect(user='root', password='toor',
#                                                host='127.0.0.1',
#                                                database='Phonebook')
#
#             print("CONNECTED")
#
#         except:
#             print("BAD Connection")
#
#         self.cursor = self.cnx.cursor()
#
#
#     def ADD(self):
#         print("ADDING DATA...")
#         nameprefix = self.nameprefix.toPlainText()
#         name = self.name.toPlainText()
#         middlename = self.middlename.toPlainText()
#         surname = self.surname.toPlainText()
#         email = self.email.toPlainText()
#         address = self.address.toPlainText()
#         phone = self.phone.toPlainText()
#         profilepath = QFileDialog.getOpenFileName(filter="*.jpg")
#         profile = profilepath.split('/')
#         print(profile[len(profile)-1])
#         os.system("cp "+profilepath+" "+path+"/ProfilePictures/"+profile[len(profile)-1])
#         print(name)
#
#         query = "INSERT INTO info(Name_prefix,Middle_Name,Surname,Email,Address,Phone,First_Name, Profile) VALUES(\"" + nameprefix + "\", \"" + middlename + "\", \"" + surname + "\", \"" + email + "\", \"" + address + "\", " + phone +", \""+name+"\", \""+profile[len(profile)-1]+"\");"
#
#         print(query)
#         self.cursor.execute(query)
#         self.cnx.commit()
#
#         # self.cnx.close()
#         MyApp.updatedata(self)
#         sys.exit()



class MyApp(QtGui.QMainWindow, Ui_MainWindow, QListWidget):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        QListWidget.__init__(self)
        QtGui.QListView.__init__(self)
        # self.listView = QListView(self)

        # self.adddata = MyAppADD(self)
        self.setupUi(self)

        # for i in range(10):
        #     self.listWidget.addItem('Item %s' % (i + 1))

        # self.listWidget.itemClicked.connect(self.ACTION)
        self.add.clicked.connect(self.ADD)
        self.search.clicked.connect(self.SEARCH)
        self.delete_2.clicked.connect(self.DELETE)
        self.refresh.clicked.connect(self.updatedata)
        self.updatedata()
        self.listWidget.itemClicked.connect(self.ACTION)
        self.Exit.clicked.connect(lambda : sys.exit())

    def updatedata(self):

        # self.listWidget.itemClicked.connect(self.ACTION)
        self.listWidget.clear()
        try:
            self.cnx = mysql.connector.connect(user='root', password='toor',
                                               host='127.0.0.1',
                                               database='Phonebook')
        except:
            print("BAD Connection")
        self.cursor = self.cnx.cursor()

        self.cursor.execute("select First_Name, Surname, Address, Email from info ORDER BY First_Name;")

        l = []

        # self.images = QLabel()


        for self.fname in self.cursor:
            print(self.fname)
            self.listWidget.addItem(self.fname[0] + " " + self.fname[1])
            l.append(self.fname)

            # a = QFileDialog.getOpenFileName().split('/')
            # print(a[len(a)-1])

    def ACTION(self):
        print("HEY")
        name = self.listWidget.selectedItems()[0].text()
        names = name.split()
        print(names)
        query = "select Address, Phone, Email, Profile from info where First_Name=\'" + names[0] + "\' and Surname=\'" + \
                names[1] + "\' ;"
        print(query)
        self.cursor.execute(query)
        result = []
        for self.data in self.cursor:
            print(self.data)
            result.append(self.data)
        print(result)
        print(name)
        if result[0][0] is None:
            self.addressset.setText("Data Not Available")
        else:
            self.addressset.setText(result[0][0])
        self.nameset.setText(name)
        self.phones.setText(str(result[0][1]))
        self.emailset.setText(result[0][2])
        self.images.setPixmap(QPixmap(path + "/ProfilePictures/" + result[0][3]))
        self.images.show()

    def ADD(self):
        # self.adddata.exec_()
        os.system("python " + path + "/add.py")

    def SEARCH(self):
        search = self.searchbox.toPlainText()

        query = "SELECT * FROM info WHERE "

        if self.byfname.isChecked():
            query += "First_Name = \"" + search + "\" ;"
        elif self.bysname.isChecked():
            query += "Surname = \"" + search + "\" ;"
        elif self.byphone.isChecked():
            query += "Phone = " + search + " ;"
        elif self.byaddress.isChecked():
            query += "Address = \"" + search + "\" ;"
        elif self.byemail.isChecked():
            query += "Email = \"" + search + "\" ;"
        elif self.bymname.isChecked():
            query += "Middle_Name = \"" + search + "\" ;"

        print(query)
        if search == "":
            self.updatedata()
        else:
            try:
                self.cursor.execute(query)

                d = []
                self.listWidget.clear()
                for self.fname in self.cursor:
                    print(self.fname)
                    self.listWidget.addItem(self.fname[2] + " " + self.fname[3])
                    d.append(self.fname)
            except:
                emsg = QMessageBox()
                emsg.setIcon(QMessageBox.Warning)

                emsg.setText("One or more fields needs attention!!")
                emsg.setInformativeText("Error While Searching")
                emsg.setWindowTitle("ERROR")
                emsg.setDetailedText("Entered field is not phone number")
                emsg.exec_()

    def DELETE(self):
        print(self.listWidget.selectedItems()[0].text())
        name = self.listWidget.selectedItems()[0].text()
        names = name.split()
        print(names)
        query = "select Address, Phone, Email, Profile from info where First_Name=\'" + names[0] + "\' and Surname=\'" + \
                names[1] + "\' ;"
        print(query)
        self.cursor.execute(query)
        result = []
        for self.data in self.cursor:
            print(self.data)
            result.append(self.data)

        print(result)

        query = "DELETE FROM info where Phone = " + str(result[0][1]) + ";"

        self.cursor.execute(query)
        self.addressset.setText("")
        self.nameset.setText("")
        self.phones.setText("")
        self.emailset.setText("")
        self.images.clear()
        self.cnx.commit()
        self.updatedata()
        os.system("rm " + path + "/ProfilePictures/" + result[0][3])


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
