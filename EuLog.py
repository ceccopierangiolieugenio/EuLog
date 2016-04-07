#!/usr/bin/python2
from __future__ import division
import sys, os
from pprint import pprint

from PyQt5 import QtCore, QtWidgets, uic
from PyQt5.QtWidgets import QFileDialog

from EuLog_mod import *

qtCreatorFile = 'ui/EuLog.main.ui'

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
	def __init__(self):
		self.fileb = None
		self.dataModel = None
		self.proxyModel = None
		self.searchesFile  = os.path.join('var','searches.txt')

		self.config = EuConfig()
		self.config.loadConfig("profiles/default.cfg")

		self.colors = EuColors()
		self.colors.loadConfig("colors/default.cfg")

		QtWidgets.QMainWindow.__init__(self)
		Ui_MainWindow.__init__(self)
		self.setupUi(self)

		self.searches = []
		self.initComboSearch()

		self.actionOpen.triggered.connect(self.openFileClicked)
		self.actionExit.triggered.connect(self.exitClicked)
		self.actionPreferences.triggered.connect(self.preferencesClicked)
		self.actionColors.triggered.connect(self.colorsClicked)
		self.txtSearchButton.clicked.connect(self.searchPattern)
		# self.comboSearchEdit.returnPressed.connect(self.searchPattern)
		# pprint (vars(self))

	def __del__(self):
		self.config.writeConfig("profiles/default.cfg")
		self.colors.writeConfig("colors/default.cfg")
		self.saveSearches()

	def exitClicked(self):
		self.close()

	def colorsClicked(self):
		d = EuColorsDialog(self.colors)
		d.exec_()
		if self.dataModel is not None:
			self.dataModel.updateConfig()
			self.proxyModel.updateConfig()

	def preferencesClicked(self):
		d = EuConfigDialog(self.config)
		d.exec_()
		if self.dataModel is not None:
			self.dataModel.updateConfig()
			self.proxyModel.updateConfig()

	def openFileClicked(self):
		if self.fileb is None:
			del self.fileb
			self.fileb = None
		filename = QFileDialog.getOpenFileName(self, "Open LogFile", ".", "Log Files (*.*)")
		if filename[0]:
			# Populate the main Table
			self.fileb = EuFileBuf(filename[0]);
			self.dataModel = EuDataModel(self.fileb, self.config, self.colors)
			self.tableView.setModel(self.dataModel)
			# Set Column width
			self.tableView.setColumnWidth(len(self.config.get('cols'))-1,800)

			# Initialize the search table
			self.proxyModel = EuDataProxyModel(self.fileb, self.config, self.colors)
			#self.proxyModel = EuDataProxyModel()
			#self.proxyModel.setSourceModel(self.dataModel)
			self.tableViewSearch.setModel(self.proxyModel)
			# Set Column width
			self.tableViewSearch.setColumnWidth(len(self.config.get('cols'))-1,800)

	def searchPattern(self):
		if self.fileb is not None :
			regex = self.comboSearchEdit.currentText()
			if regex not in self.searches:
				self.searches.insert(0,regex)
				self.comboSearchEdit.insertItem(0,regex)
			indexes = self.fileb.search('.*'+regex)
			self.proxyModel.euSetIndexes(indexes)

	def initComboSearch(self):
		if os.path.isfile(self.searchesFile) :
			with open(self.searchesFile,'r') as infile:
				for line in infile:
					self.searches.append(line.strip('\n'))
					self.comboSearchEdit.insertItem(0,line.strip('\n'))

	def saveSearches(self):
		# Save only the last 100 elements
		with open(self.searchesFile,'w') as outfile:
			for txt in self.searches[0:100]:
				outfile.write(txt+'\n')

if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	window = MyApp()
	window.show()
	sys.exit(app.exec_())




