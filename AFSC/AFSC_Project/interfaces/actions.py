# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'actions.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ac(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(415, 119)
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(90, 70, 89, 25))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(200, 70, 89, 25))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(Form)
        self.pushButton_3.setGeometry(QtCore.QRect(310, 70, 89, 25))
        self.pushButton_3.setObjectName("pushButton_3")
        self.spinBox = QtWidgets.QSpinBox(Form)
        self.spinBox.setGeometry(QtCore.QRect(20, 70, 48, 26))
        self.spinBox.setObjectName("spinBox")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(20, 50, 67, 17))
        self.label.setObjectName("label")
        self.pushButton_13 = QtWidgets.QPushButton(Form)
        self.pushButton_13.setGeometry(QtCore.QRect(0, 0, 31, 31))
        self.pushButton_13.setStyleSheet("QPushButton{\n"
"background-color:rgb(114, 159, 207);\n"
" color: white;\n"
" \n"
" font-size: 16px;\n"
"}\n"
"QPushButton:hover{\n"
"background-color:rgb(52, 101, 164);\n"
"color:white;\n"
"}")
        self.pushButton_13.setIconSize(QtCore.QSize(64, 64))
        self.pushButton_13.setObjectName("pushButton_13")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.pushButton.setText(_translate("Form", "Start"))
        self.pushButton_2.setText(_translate("Form", "Stop"))
        self.pushButton_3.setText(_translate("Form", "Snapshot"))
        self.label.setText(_translate("Form", "Vm ID"))
        self.pushButton_13.setText(_translate("Form", "<-"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ac()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

