# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ListVMs.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class ListVm(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(525, 384)
        self.textEdit = QtWidgets.QTextEdit(Form)
        self.textEdit.setGeometry(QtCore.QRect(10, 40, 511, 331))
        self.textEdit.setObjectName("textEdit")
        self.pushButton_11 = QtWidgets.QPushButton(Form)
        self.pushButton_11.setGeometry(QtCore.QRect(0, 0, 31, 31))
        self.pushButton_11.setStyleSheet("QPushButton{\n"
"background-color:rgb(114, 159, 207);\n"
" color: white;\n"
" \n"
" font-size: 16px;\n"
"}\n"
"QPushButton:hover{\n"
"background-color:rgb(52, 101, 164);\n"
"color:white;\n"
"}")
        self.pushButton_11.setIconSize(QtCore.QSize(64, 64))
        self.pushButton_11.setObjectName("pushButton_11")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.pushButton_11.setText(_translate("Form", "<-"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = ListVm()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

