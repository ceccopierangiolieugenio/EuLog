#!/usr/bin/python2
from __future__ import division
import sys
from pprint import pprint

from PyQt5 import QtCore, QtWidgets, uic
from PyQt5.QtWidgets import QFileDialog

from EuLog_mod import *

#
# TEST;0:17:06;COL1	COL2     COL3  c:COL4;LIN=0001A	RND=0.480630  Fill Fill Fill
# xxxx;xxxxxxx;xxxx\txxxxxxx     xxxx  c:xxxx;....
# ID   Time    COL1     COL2     COL3    COL4 TXT
tmp_regex = '([^;]*);([^;]*);([^\t]*)\t([^ ]*)     ([^ ]*)  c:([^;]*);(.*)'
tmp_cols = ["ID","Time","COL1","COL2","COL3","COL4","TXT"]

qtCreatorFile = "ui/EuLog.main.ui"

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
	def __init__(self):
		self.fileb = None
		QtWidgets.QMainWindow.__init__(self)
		Ui_MainWindow.__init__(self)
		self.setupUi(self)
		self.actionOpen.triggered.connect(self.OpenFileClicked)
		self.txtSearchButton.clicked.connect(self.SearchPattern)
		self.txtSearchEdit.returnPressed.connect(self.SearchPattern)
		# pprint (vars(self))

	def OpenFileClicked(self):
		if self.fileb is None:
			del self.fileb
			self.fileb = None
		filename = QFileDialog.getOpenFileName(self, "Open LogFile", ".", "Log Files (*.*)")
		print filename
		if filename[0]:
			self.fileb = EuFileBuf(filename[0]);
			dataModel = EuDataModel(self.fileb, tmp_regex, tmp_cols)
			self.tableView.setModel(dataModel)

	def SearchPattern(self):
		if self.fileb is not None :
			regex = self.txtSearchEdit.text()
			indexes = self.fileb.Search('.*'+regex)
			dataModelSearch = EuDataModelSearch(self.fileb, tmp_regex, tmp_cols, indexes)
			self.tableViewSearch.setModel(dataModelSearch)

if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	window = MyApp()
	window.show()
	sys.exit(app.exec_())




