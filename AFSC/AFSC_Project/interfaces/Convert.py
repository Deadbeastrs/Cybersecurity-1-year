# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Convert.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Conv(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 218)
        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setGeometry(QtCore.QRect(20, 40, 271, 25))
        self.lineEdit.setObjectName("lineEdit")
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(300, 40, 89, 25))
        self.pushButton.setObjectName("pushButton")
        self.radioButton = QtWidgets.QRadioButton(Form)
        self.radioButton.setGeometry(QtCore.QRect(30, 90, 112, 23))
        self.radioButton.setObjectName("radioButton")
        self.radioButton_2 = QtWidgets.QRadioButton(Form)
        self.radioButton_2.setGeometry(QtCore.QRect(30, 130, 112, 23))
        self.radioButton_2.setObjectName("radioButton_2")
        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(150, 170, 89, 25))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_12 = QtWidgets.QPushButton(Form)
        self.pushButton_12.setGeometry(QtCore.QRect(0, 0, 31, 31))
        self.pushButton_12.setStyleSheet("QPushButton{\n"
"background-color:rgb(114, 159, 207);\n"
" color: white;\n"
" \n"
" font-size: 16px;\n"
"}\n"
"QPushButton:hover{\n"
"background-color:rgb(52, 101, 164);\n"
"color:white;\n"
"}")
        self.pushButton_12.setIconSize(QtCore.QSize(64, 64))
        self.pushButton_12.setObjectName("pushButton_12")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.pushButton.setText(_translate("Form", "Select file"))
        self.radioButton.setText(_translate("Form", "Vdi to Vmdk"))
        self.radioButton_2.setText(_translate("Form", "Vmdk to VDI"))
        self.pushButton_2.setText(_translate("Form", "Go"))
        self.pushButton_12.setText(_translate("Form", "<-"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Conv()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

