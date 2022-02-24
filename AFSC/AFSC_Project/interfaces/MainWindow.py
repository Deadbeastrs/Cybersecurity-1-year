# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class MainW(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(606, 407) 
        Form.setStyleSheet("background-color: rgb(238, 238, 236);")
        self.pushButton_3 = QtWidgets.QPushButton(Form)
        self.pushButton_3.setGeometry(QtCore.QRect(240, 60, 121, 111))
        self.pushButton_3.setStyleSheet("QPushButton{\n"
"border: 5px solid gb(85, 87, 83);\n"
"border-radius: 14px;\n"
"background-color: (238, 238, 236);\n"
" color: white;\n"
" padding: 14px 28px;\n"
" font-size: 16px;\n"
"}\n"
"QPushButton:hover{\n"
"background-color:rgb(136, 138, 133);\n"
"color:black;\n"
"}")
        self.pushButton_3.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icons/vms.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_3.setIcon(icon)
        self.pushButton_3.setIconSize(QtCore.QSize(64, 64))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_9 = QtWidgets.QPushButton(Form)
        self.pushButton_9.setGeometry(QtCore.QRect(30, 60, 121, 111))
        self.pushButton_9.setStyleSheet("QPushButton{\n"
"border: 5px solid gb(85, 87, 83);\n"
"border-radius: 14px;\n"
"background-color: (238, 238, 236);\n"
" color: white;\n"
" padding: 14px 28px;\n"
" font-size: 16px;\n"
"}\n"
"QPushButton:hover{\n"
"background-color:rgb(136, 138, 133);\n"
"color:black;\n"
"}")
        self.pushButton_9.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("icons/inspect.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_9.setIcon(icon1)
        self.pushButton_9.setIconSize(QtCore.QSize(64, 64))
        self.pushButton_9.setObjectName("pushButton_9")
        self.pushButton_4 = QtWidgets.QPushButton(Form)
        self.pushButton_4.setGeometry(QtCore.QRect(450, 60, 121, 111))
        self.pushButton_4.setStyleSheet("QPushButton{\n"
"border: 5px solid gb(85, 87, 83);\n"
"border-radius: 14px;\n"
"background-color: (238, 238, 236);\n"
" color: white;\n"
" padding: 14px 28px;\n"
" font-size: 16px;\n"
"}\n"
"QPushButton:hover{\n"
"background-color:rgb(136, 138, 133);\n"
"color:black;\n"
"}")
        self.pushButton_4.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("icons/convert.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_4.setIcon(icon2)
        self.pushButton_4.setIconSize(QtCore.QSize(64, 64))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_5 = QtWidgets.QPushButton(Form)
        self.pushButton_5.setGeometry(QtCore.QRect(130, 230, 121, 111))
        self.pushButton_5.setStyleSheet("QPushButton{\n"
"border: 5px solid gb(85, 87, 83);\n"
"border-radius: 14px;\n"
"background-color: (238, 238, 236);\n"
" color: white;\n"
" padding: 14px 28px;\n"
" font-size: 16px;\n"
"}\n"
"QPushButton:hover{\n"
"background-color:rgb(136, 138, 133);\n"
"color:black;\n"
"}")
        self.pushButton_5.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("icons/actions.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_5.setIcon(icon3)
        self.pushButton_5.setIconSize(QtCore.QSize(90, 100))
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_6 = QtWidgets.QPushButton(Form)
        self.pushButton_6.setGeometry(QtCore.QRect(350, 230, 121, 111))
        self.pushButton_6.setStyleSheet("QPushButton{\n"
"border: 5px solid gb(85, 87, 83);\n"
"border-radius: 14px;\n"
"background-color: (238, 238, 236);\n"
" color: white;\n"
" padding: 14px 28px;\n"
" font-size: 16px;\n"
"}\n"
"QPushButton:hover{\n"
"background-color:rgb(136, 138, 133);\n"
"color:black;\n"
"}")
        self.pushButton_6.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("icons/report.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_6.setIcon(icon4)
        self.pushButton_6.setIconSize(QtCore.QSize(90, 100))
        self.pushButton_6.setObjectName("pushButton_6")
        self.pushButton_10 = QtWidgets.QPushButton(Form)
        self.pushButton_10.setGeometry(QtCore.QRect(570, 0, 31, 31))
        self.pushButton_10.setStyleSheet("QPushButton{\n"
"background-color:rgb(114, 159, 207);\n"
" color: white;\n"
" \n"
" font-size: 16px;\n"
"}\n"
"QPushButton:hover{\n"
"background-color:rgb(52, 101, 164);\n"
"color:white;\n"
"}")
        self.pushButton_10.setIconSize(QtCore.QSize(64, 64))
        self.pushButton_10.setObjectName("pushButton_10")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(70, 180, 51, 21))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(150, 350, 91, 21))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(280, 180, 41, 21))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(350, 350, 141, 21))
        self.label_4.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_4.setLineWidth(13)
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(Form)
        self.label_5.setGeometry(QtCore.QRect(490, 180, 61, 21))
        self.label_5.setObjectName("label_5")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.pushButton_10.setText(_translate("Form", "?"))
        self.label.setText(_translate("Form", "vmdisk"))
        self.label_2.setText(_translate("Form", "vmactions"))
        self.label_3.setText(_translate("Form", "vmlist"))
        self.label_4.setText(_translate("Form", " Generate report"))
        self.label_5.setText(_translate("Form", "convert"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = MainW()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

