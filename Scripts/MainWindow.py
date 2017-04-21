#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
In this example, we create a simple
window in PyQt5.

author: Kardo Aziz

"""

from PyQt5.QtWidgets import * #QApplication, QWidget,QAction, qApp, QPushButton, QMessageBox,QMainWindow
from PyQt5.QtCore import *
from PyQt5 import QtGui, QtCore
import PySide
from PySide import QtGui
from rpy2.robjects.packages import importr
import gui as R
import preparedata as pre
import DB_Activities as db
class MainWindow(QMainWindow):
	def __init__(self,height,width):
		super(MainWindow,self).__init__()
		self.height = height
		self.width = width
		self.companies = QComboBox(self)
		self._1day = QCheckBox("Tomorrow",self)
		self._2day = QCheckBox("2 days",self)
		self._3day = QCheckBox("3 days",self)
		self.Model2 = QCheckBox("Use Second model (Slower)",self)
		self._UseCompanies = QCheckBox("Check to use companies",self)
		self.fileStatus = QLabel("No File Loaded  OR",self)
		self.CurrentFile = ""
		self.CurrentFile2 = ""
		self.use_Companies = False
		self.DefaultCompany = [0,'Facebook']
		self.resultlbl = QLabel("Predicted Result will appear HERE",self)
		self.createUI()
		self.addCompany = QPushButton("Add New Company")
		self.model = 1
		self.vbox = None
		self.comp = ""
	def createUI(self):
		self.setWindowTitle('Equipment Manager 0.3')
		try:
			menuFile = self.menuBar().addMenu('File')
			#menuAbout = self.menuBar().addMenu('aAbout')
			menuHelp = self.menuBar().addMenu('Help')
			
			_open = menuFile.addAction('Open')
			_open.triggered.connect(self.showDialog) 

			_load = menuFile.addAction('Load')
			_load.triggered.connect(self.showDialog)  

			_clear = menuFile.addAction('Clear')
			_clear.triggered.connect(self.clearWindow)  

			_save = menuFile.addAction('Save')
			_save.triggered.connect(self.saveModel)  

			_exit = menuFile.addAction('Close')
			_exit.triggered.connect(self.close)  

			_help = menuHelp.addAction('Help')
			_help.triggered.connect(self.close)  

			we = menuHelp.addAction('about us')
			#we.triggered.connect(self.close)    

			# self.toolbar =self.addToolBar('Close')
			# self.toolbar.addAction(_exit)

			btnLoad = QPushButton('Load')
			self.CurrentFile = btnLoad.clicked.connect(self.showDialog)
			btnPredict = QPushButton('Predict')
			btnPredict.clicked.connect(self.predict)
			btnClear = QPushButton('Clear')
			addCompany = QPushButton('Add New Company')
			addCompany.clicked.connect(self.addNewCompany)
			btnClear.clicked.connect(self.clearWindow)

			self.Model2.stateChanged.connect(self.useModel2)
			self.changeStatus("ready")
			
			self._UseCompanies.stateChanged.connect(self.useCompanies)
			companies = db.getCompanies()
			for s in companies :

				self.companies.addItem(s)
			# self.companies.addItem("Google")
			# self.companies.addItem("Apple")
			self.companies.currentIndexChanged.connect(self.selectionChanged)
			hbox1 = QHBoxLayout(self)

			hbox2 = QHBoxLayout(self)
			hbox3 = QHBoxLayout(self)

			hbox2.addWidget(btnPredict)
			self._1day.setChecked(True)
			hbox2.addWidget(self._1day)
			hbox2.addWidget(self.Model2)
			# hbox2.addWidget(self._2day)
			# hbox2.addWidget(self._3day)

			hbox1.addWidget(btnLoad)
			hbox1.addWidget(self.fileStatus)
			hbox1.addWidget(addCompany)
			hbox1.addWidget(self.companies)
			hbox1.addWidget(self._UseCompanies)

			hbox3.addWidget(self.resultlbl)
			hbox3.addWidget(btnClear)

			self.vbox = QVBoxLayout(self)
			# hbox3.addWidget(p)
			self.vbox.addLayout(hbox1)
			self.vbox.addLayout(hbox2)
			self.vbox.addLayout(hbox3)

			w = QWidget()
			w.setLayout(self.vbox)

			self.setCentralWidget(w)

		except IOError as e:
			print(e)


	# def closeEvent(self,event):
	# 	reply = QMessageBox.question(self,'Message',
	# 								'Are you sure ?',
	# 								QMessageBox.Yes |
	# 								QMessageBox.No,
	# 								QMessageBox.No)
	def useCompanies(self,checked):
		self.use_Companies = (checked == True)
		print("Using companies : {}".format(checked))
		#print(pre.readDataDB(self.companies.currentText()))
	def addNewCompany(self):
		if(self.comp != ""):
			data = pre.readData(self.comp)
			while True:
				text ,ok = QInputDialog.getText(self,'Input Dialog', 'Enter Company name')
				if ok :
					if text != "" and text  not in db.getCompanies() :
						print(text)

						db.add_company(text)
						db.add_data_to_Company(text,data)
						self.companies.addItem(text)
						self._UseCompanies.setChecked(True)
						break
					else:
						QMessageBox.information(self,"Warning","The company id already exist")
				else:
					break
		else:
			QMessageBox.information(self,"Warning","Please load a Data first")

	def useModel2(self,checked):
		if checked :
			self.model = 2
		else :
			self.model = 1
		print("Model `: {}".format(self.model))
	def changeStatus(self,text):
		self.statusBar().showMessage(text)

	def LoadFile(self):
		self.changeStatus("Loading File...")
		print("LoadFile Clicked")
		self.changeStatus("File Loaded")

	def predict(self):
		self.changeStatus("Predicting...")
		print("Predict Clicked")
		if self._UseCompanies.isChecked():
			comp = self.companies.currentText()

			#self.CurrentFile = 
			data = pre.readDataDB(comp)		
			pre.generateData(data,3)
			pre.generateData2(data,4)
			self.CurrentFile = "../Data/data_3_days.csv"
			self.CurrentFile2 = "../Data/data2_4_days.csv"
		# print(self.CurrentFile)
		if self.CurrentFile == "" or self.CurrentFile == None:
			self.changeStatus("No File Loaded ..!")
		else:
			# print("File path {}".format(self.CurrentFile))
			if self.model == 1 :
				price = R.mainFunction(self.CurrentFile,self.model)
			else:
				price = R.mainFunction(self.CurrentFile2,self.model)

			self.changeStatus("Predicted : {}".format(price))
			self.resultlbl.setText("Tomorrow's price will be {}".format(price))
			self.resultlbl.setStyleSheet('color : green')
			

	def saveModel(self):
		self.changeStatus("Saving Model...")
		print("Save Model Clicked")
		self.changeStatus("Model saved")

	def openModel(self):
		self.changeStatus("Opening Model...")
		print("Open Model Clicked")
		self.changeStatus("Model Loaded")

	def showDialog(self):
		file = QFileDialog.getOpenFileName(self,'Open File', '/home/RIT/Sprint_2016/Big Data/StockValue/Stock_Value_Project')
		# print(file[0])
		self.comp = file[0]
		data = pre.readData(file[0])		
		pre.generateData(data,3)
		pre.generateData2(data,4)

		self.changeStatus(file[0])
		last = file[0].rfind('/')
		self.fileStatus.setText(file[0][last+1:])
		if(self._UseCompanies.isChecked()):
			self._UseCompanies.setChecked(False)
		self.CurrentFile2 = "../Data/data2_4_days.csv"
		
		self.CurrentFile = "../Data/data_3_days.csv"
		print("File : {}".format(self.CurrentFile))
		return self.CurrentFile,self.CurrentFile2

	def selectionChanged(self,i):
		self.DefaultCompany = [i,self.companies.currentText()]
		#print("Index : {} , Item : {}".format(i, self.companies.currentText()))
		print(self.DefaultCompany)
		self._UseCompanies.setChecked(True)
		self.changeStatus("{} Data is loaded".format(self.companies.currentText()))

	def clearWindow(self):
		self.DefaultCompany = [0, 'Facebook']
		self._1day.setChecked(True)
		self._2day.setChecked(False)
		self._3day.setChecked(False)
		self._UseCompanies.setChecked(False)
		self.fileStatus.setText('No File Loaded  OR')
		self.changeStatus("Ready")
		self.CurrentFile = ""
		self.CurrentFile2 = ""
		self.resultlbl.setText("Predicted Result will appear HERE")

if __name__ == '__main__':

	import sys
	app = QApplication(sys.argv)
	height = 300
	width = 300
	window = MainWindow(height,width)
	window.show()
	 
	window.setGeometry(height, width, 800, 500)
	sys.exit(app.exec_()) 