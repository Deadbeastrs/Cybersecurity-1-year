### System

import shutil
import os
from subprocess import Popen, PIPE, STDOUT
from typing import ClassVar
import webbrowser


### PyQt5

from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg

### Interfaces
from interfaces.MainWindow import MainW
from interfaces.ListVMs import ListVm
from interfaces.Convert import Conv
from interfaces.actions import Ac
from interfaces.ConvertWin import ConvW

class MainWindow(qtw.QWidget):

    def __init__(self, widget, *args, **kwargs):
        super().__init__(*args,**kwargs)

        self.ui = MainW()
        self.ui.setupUi(self)
        self.ui.pushButton_3.clicked.connect(self.vms)
        self.ui.pushButton_9.clicked.connect(self.disks)
        self.ui.pushButton_6.clicked.connect(self.report)
        self.ui.pushButton_4.clicked.connect(self.convert)
        self.ui.pushButton_10.clicked.connect(self.help)
        self.ui.pushButton_5.clicked.connect(self.act)
        self.widget = widget
        

    def vms(self):
        if os.name != 'nt':
            
            p = Popen(['./tool'], stdout=PIPE,stdin=PIPE,stderr=PIPE)
            stdout_data = p.communicate(input = 'vmlist\nexit'.encode())[0]
            info = str(stdout_data.decode('UTF-8'))
            max = self.widget.count()
            for i in range(max):
                self.widget.removeWidget(self.widget.widget(max-i))

            main = ListMachines(self.widget,info)
            self.widget.addWidget(main)
            self.widget.setCurrentIndex(1)
            self.widget.setFixedHeight(384)
            self.widget.setFixedWidth(525)
        else:
           
            p = Popen(["powershell.exe", ".\Forense.ps1"], stdout=PIPE,stdin=PIPE,stderr=PIPE)
            stdout_data = p.communicate(input = 'R\r\nn\r\nvmlist\r\nexit'.encode())[0]
            info = str(stdout_data.decode('UTF-8'))
            print("-----------------------------------------")
            print(info)
            max = self.widget.count()
            for i in range(max):
                self.widget.removeWidget(self.widget.widget(max-i))

            main = ListMachines(self.widget,info)
            self.widget.addWidget(main)
            self.widget.setCurrentIndex(1)
            self.widget.setFixedHeight(384)
            self.widget.setFixedWidth(525)
    def disks(self):
        if os.name != 'nt':
           
            p = Popen(['./tool'], stdout=PIPE,stdin=PIPE,stderr=PIPE)
            stdout_data = p.communicate(input = 'vmdisks\nexit'.encode())[0]
            info = str(stdout_data.decode('UTF-8'))
            max = self.widget.count()
            for i in range(max):
                self.widget.removeWidget(self.widget.widget(max-i))

            main = ListMachines(self.widget,info)
            self.widget.addWidget(main)
            self.widget.setCurrentIndex(1)
            self.widget.setFixedHeight(384)
            self.widget.setFixedWidth(525)
        else:
            p = Popen(["powershell.exe", ".\Forense.ps1"], stdout=PIPE,stdin=PIPE,stderr=PIPE)
            #p.stdin.write('R\r\nn\r\nvmdisk\r\nexit\r\n')
            stdout_data = p.communicate(input = 'R\r\nn\r\nvmdisk\r\nexit'.encode())[0]
            info = str(stdout_data.decode('UTF-8'))
            print("-----------------------------------------")
            print(info)
            max = self.widget.count()
            for i in range(max):
                self.widget.removeWidget(self.widget.widget(max-i))

            main = ListMachines(self.widget,info)
            self.widget.addWidget(main)
            self.widget.setCurrentIndex(1)
            self.widget.setFixedHeight(384)
            self.widget.setFixedWidth(525)

    def report(self):

        if os.name != 'nt':
            
            p = Popen(['./tool'], stdout=PIPE,stdin=PIPE,stderr=PIPE)
            stdout_data = p.communicate(input = 'gen_report\nreport\nexit'.encode())[0]
            path = os.path.abspath(os.getcwd())
            url = 'file://'+ path+ '/report.html'
            webbrowser.open(url, new=2)  
        else: 
            p = Popen(["powershell.exe", ".\Forense.ps1"], stdout=PIPE,stdin=PIPE,stderr=PIPE)
            stdout_data = p.communicate(input = 'R\r\nn\r\ngen_report\r\nexit'.encode())[0]
         
            url = 'C:\\report.html'
            webbrowser.open(url, new=2)
    def convert(self):
        
        max = self.widget.count()
        for i in range(max):
            self.widget.removeWidget(self.widget.widget(max-i))

        main = Converter(self.widget)
        self.widget.addWidget(main)
        self.widget.setCurrentIndex(1)
        self.widget.setFixedHeight(218)
        self.widget.setFixedWidth(400)



    def help(self):
        msgBox = qtw.QMessageBox()
        msgBox.setIcon(qtw.QMessageBox.Information)
        msgBox.setText("Available Tools: \n\nvmlist        - list all virtual machines \nvmdisks       - list all virtual machines disks in system \nvmactions     - actions on all virtual machines running\nvdi_vmdk      - convert vmi to vmdk or vice versa\ngen_report    - generate a report with the VM's information\nhelp          - display the menu \nexit          - closes the script")
        msgBox.setWindowTitle("Help")
        msgBox.setStandardButtons(qtw.QMessageBox.Ok)
        msgBox.buttonClicked.connect(self.msgbtn)
        retval = msgBox.exec()

    def msgbtn(self):
        return None

    def act(self):
        max = self.widget.count()
        for i in range(max):
            self.widget.removeWidget(self.widget.widget(max-i))

        main = Actions(self.widget)
        self.widget.addWidget(main)
        self.widget.setCurrentIndex(1)
        self.widget.setFixedHeight(119)
        self.widget.setFixedWidth(415)

class ListMachines(qtw.QWidget):

    def __init__(self, widget,info, *args, **kwargs):
        super().__init__(*args,**kwargs)

        self.ui = ListVm()
        self.ui.setupUi(self)
        self.widget = widget
        self.ui.textEdit.setText(info.split("Choose an option:")[1])
        self.ui.pushButton_11.clicked.connect(self.goBack)

    def goBack(self):
        max = self.widget.count()
        for i in range(max):
            self.widget.removeWidget(self.widget.widget(max-i))

        main = MainWindow(self.widget)
        self.widget.addWidget(main)
        self.widget.setCurrentIndex(1)
        self.widget.setFixedHeight(407)
        self.widget.setFixedWidth(606)

class Converter(qtw.QWidget):

    def __init__(self, widget, *args, **kwargs):
        super().__init__(*args,**kwargs)

        self.ui = Conv()
        self.ui.setupUi(self)
        self.widget = widget
        self.path = ""
        self.ui.pushButton_12.clicked.connect(self.goBack)
        self.ui.pushButton.clicked.connect(self.getPath)
        self.ui.pushButton_2.clicked.connect(self.convert)
        
        if os.name == 'nt':
            self.ui.radioButton.setText("vhd to vhdx")
            self.ui.radioButton_2.setText("vhdx to vhd")

        
    def goBack(self):
        max = self.widget.count()
        for i in range(max):
            self.widget.removeWidget(self.widget.widget(max-i))

        main = MainWindow(self.widget)
        self.widget.addWidget(main)
        self.widget.setCurrentIndex(1)
        self.widget.setFixedHeight(407)
        self.widget.setFixedWidth(606)

    def getPath(self):
        files = qtw.QFileDialog.getOpenFileName(self)
        filename = files[0]
        self.ui.lineEdit.setText(str(filename))
        self.path = str(filename)
    
    def convert(self):
        if os.name != 'nt':
            
            if self.ui.radioButton.isChecked():

                p = Popen(['./tool'], stdout=PIPE,stdin=PIPE,stderr=PIPE)
                stdout_data = p.communicate(input = ('vdi_vmdk\nvdi_vmdk '+str(self.path) + ' ' + str(self.path.split("/")[-1]) + '.vmdk ' + '\nexit').encode())[0]
                
            elif self.ui.radioButton_2.isChecked():

                p = Popen(['./tool'], stdout=PIPE,stdin=PIPE,stderr=PIPE)
                stdout_data = p.communicate(input = ('vdi_vmdk\nvmdk_vdi '+str(self.path) + ' ' + str(self.path.split("/")[-1]) + '.vdi ' + '\nexit').encode())[0]
                
        else:
            #print(('R\r\nn\r\nvhd_vhdx\r\n '+str(self.path).replace('/','\\') + '\r\n ' +str(os.path.abspath(os.getcwd())) + 'vhd\r\n\r\nexit'))
            if self.ui.radioButton.isChecked():
                p = Popen(["powershell.exe", ".\Forense.ps1"], stdout=PIPE,stdin=PIPE,stderr=PIPE)
                stdout_data = p.communicate(input = ('R\r\nn\r\nvhd_vhdx\r\n '+str(self.path).replace('/','\\') + '\r\n ' +str(os.path.abspath(os.getcwd())) +'\\'+ str(self.path.split("/")[-1]) + '\r\nvhdx\r\n\r\n\r\n\r\nexit').encode())[0]
                
            elif self.ui.radioButton_2.isChecked():
                p = Popen(["powershell.exe", ".\Forense.ps1"], stdout=PIPE,stdin=PIPE,stderr=PIPE)
                stdout_data = p.communicate(input = ('R\r\nn\r\nvhd_vhdx\r\n '+str(self.path).replace('/','\\') + '\r\n ' +str(os.path.abspath(os.getcwd())) +'\\'+ str(self.path.split("/")[-1]) + '\r\nvhd\r\n\r\n\r\n\r\nexit').encode())[0]


class Actions(qtw.QWidget):

    def __init__(self, widget, *args, **kwargs):
        super().__init__(*args,**kwargs)

        self.ui = Ac()
        self.ui.setupUi(self)
        self.widget = widget
        self.ui.pushButton_13.clicked.connect(self.goBack)
        self.ui.pushButton.clicked.connect(self.start)
        self.ui.pushButton_2.clicked.connect(self.stop)
        self.ui.pushButton_3.clicked.connect(self.snap)
       
    def start(self):
        if os.name != 'nt':
            print('vmactions\nstart ' + str(self.ui.spinBox.value()) + '\nexit')
            p = Popen(['./tool'], stdout=PIPE,stdin=PIPE,stderr=PIPE)
            stdout_data = p.communicate(input = ('vmactions\nstart ' + str(self.ui.spinBox.value()) + '\nexit').encode())[0]

        else:
            p = Popen(["powershell.exe", ".\Forense.ps1"], stdout=PIPE,stdin=PIPE,stderr=PIPE)
            stdout_data = p.communicate(input = ('R\r\nn\r\nvmactions\r\n' + str(self.ui.spinBox.value()) + '\r\nstart\r\n\r\nexit').encode())[0]


    def stop(self):
        if os.name != 'nt':
            print('vmactions\nstart ' + str(self.ui.spinBox.value()) + '\nexit')
            p = Popen(['./tool'], stdout=PIPE,stdin=PIPE,stderr=PIPE)
            stdout_data = p.communicate(input = ('vmactions\nstop ' + str(self.ui.spinBox.value()) + '\nexit').encode())[0]

        else:
            p = Popen(["powershell.exe", ".\Forense.ps1"], stdout=PIPE,stdin=PIPE,stderr=PIPE)
            stdout_data = p.communicate(input = ('R\r\nn\r\nvmactions\r\n'+str(self.ui.spinBox.value())+'\r\nstop\r\n\r\nexit').encode())[0]
    def snap(self):

        if os.name != 'nt':
            print('vmactions\nstart ' + str(self.ui.spinBox.value()) + '\nexit')
            p = Popen(['./tool'], stdout=PIPE,stdin=PIPE,stderr=PIPE)
            stdout_data = p.communicate(input = ('vmactions\nsnapshot ' + str(self.ui.spinBox.value()) + '\nexit').encode())[0]

        else:
            p = Popen(["powershell.exe", ".\Forense.ps1"], stdout=PIPE,stdin=PIPE,stderr=PIPE)
            stdout_data = p.communicate(input = ('R\r\nn\r\nvmactions\r\n'+str(self.ui.spinBox.value())+'\r\nsnapshot\r\n\r\nexit').encode())[0]
    def goBack(self):
        max = self.widget.count()
        for i in range(max):
            self.widget.removeWidget(self.widget.widget(max-i))

        main = MainWindow(self.widget)
        self.widget.addWidget(main)
        self.widget.setCurrentIndex(1)
        self.widget.setFixedHeight(407)
        self.widget.setFixedWidth(606)
        