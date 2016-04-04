#!/usr/bin/python2
from __future__ import division
import sys, os
from pprint import pprint

from PyQt5 import QtCore, QtWidgets, uic
from PyQt5.QtWidgets import QFileDialog

from EuLog_mod import *

#
# TEST;0:17:06;COL1	COL2     COL3  c:COL4;LIN=0001A	RND=0.480630  Fill Fill Fill
# xxxx;xxxxxxx;xxxx\txxxxxxx     xxxx  c:xxxx;....
# ID   Time    COL1     COL2     COL3    COL4 TXT
# tmp_regex = '([^;]*);([^;]*);([^\t]*)\t([^ ]*)     ([^ ]*)  c:([^;]*);(.*)'
# tmp_cols = ["ID","Time","COL1","COL2","COL3","COL4","TXT"]

qtCreatorFile = "ui/EuLog.main.ui"

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
	def __init__(self):
		self.fileb = None

		self.config = EuConfig()
		self.config.loadConfig("profiles/default.cfg")
		# self.config.writeConfig("profiles/default.cfg")

		QtWidgets.QMainWindow.__init__(self)
		Ui_MainWindow.__init__(self)
		self.setupUi(self)

		self.searches = []
		self.initComboSearch()

		self.actionOpen.triggered.connect(self.openFileClicked)
		self.actionExit.triggered.connect(self.exitClicked)
		self.txtSearchButton.clicked.connect(self.searchPattern)
		# self.comboSearchEdit.returnPressed.connect(self.searchPattern)
		# pprint (vars(self))

	def __del__(self):
		self.saveSearches()

	def exitClicked(self):
		self.close()

	def openFileClicked(self):
		if self.fileb is None:
			del self.fileb
			self.fileb = None
		filename = QFileDialog.getOpenFileName(self, "Open LogFile", ".", "Log Files (*.*)")
		print(filename)
		if filename[0]:
			self.fileb = EuFileBuf(filename[0]);
			dataModel = EuDataModel(self.fileb, self.config.get('regex'), self.config.get('cols'))
			self.tableView.setModel(dataModel)
			# Set Column width
			self.tableView.setColumnWidth(len(self.config.get('cols'))-1,800)

	def searchPattern(self):
		if self.fileb is not None :
			regex = self.comboSearchEdit.currentText()
			self.searches.insert(0,regex)
			self.comboSearchEdit.insertItem(0,regex)
			indexes = self.fileb.search('.*'+regex)
			dataModelSearch = EuDataModelSearch(self.fileb, self.config.get('regex'), self.config.get('cols'), indexes)
			self.tableViewSearch.setModel(dataModelSearch)
			self.tableViewSearch.setColumnWidth(len(self.config.get('cols'))-1,800)

	def initComboSearch(self):
		if os.path.isfile('var/searches.txt') :
			with open('var/searches.txt','r') as infile:
				for line in infile:
					self.searches.append(line.strip('\n'))
					self.comboSearchEdit.insertItem(0,line.strip('\n'))

	def saveSearches(self):
		outfile = open('var/searches.txt','w')
		# Save only the last 100 elements
		for txt in self.searches[0:100]:
			outfile.write(txt+'\n')

if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	window = MyApp()
	window.show()
	sys.exit(app.exec_())




