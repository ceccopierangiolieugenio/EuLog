import sip, os

from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import Qt, QVariant
from PyQt5.QtWidgets import *

qtCreatorFile = 'ui/EuLog.Config.ui'

Ui_ConfigDiag, QtBaseClass = uic.loadUiType(qtCreatorFile)

class EuConfigDialog(QDialog, Ui_ConfigDiag):
	def __init__(self, config):
		self.config = config
		QDialog.__init__(self)
		Ui_ConfigDiag.__init__(self)
		self.setupUi(self)
		self.setWindowModality(Qt.ApplicationModal)
		self.initUI()
		self.show()

	def initUI(self):
		# Add the default.cfg on top of the combo list also if it
		# doesn't exists, I know it is stupid but I'm to tired now
		# to look for a better solution
		self.profilesComboBox.insertItem(1, 'default.cfg')
		for files in os.listdir('profiles'):
			if files != 'default.cfg':
				self.profilesComboBox.insertItem(1, files)

		self.c_hLayCol = []
		self.setConfig()

		self.addColumnButton.clicked.connect(self.addColumn)
		self.removeColumnButton.clicked.connect(self.removeColumn)
		self.okButton.clicked.connect(self.saveAndClose)
		self.profilesComboBox.currentIndexChanged.connect(self.profileChanged)

		QtCore.QMetaObject.connectSlotsByName(self)

	def saveAndClose(self):
		profile = self.profilesComboBox.currentText()
		self.config.set('regex',self.lineEditRegex.text())
		cols = []
		for key, col in enumerate(self.c_hLayCol):
			cols.append(col.colName.text())
			if col.radioDef.isChecked():
				self.config.set('default', key)
		self.config.set('cols',cols)
		self.config.writeConfig(os.path.join('profiles','default.cfg'))
		self.config.writeConfig(os.path.join('profiles',profile))
		self.close()

	def setConfig(self):
		self.removeAllColumns()
		self.genColsLayout()
		self.lineEditRegex.setText(self.config.get('regex'))

	def profileChanged(self, val):
		profile = self.profilesComboBox.itemText(val)
		self.config.loadConfig(os.path.join('profiles',profile))
		self.setConfig()

	def addColumn(self):
		self.addColLayout("")

	def removeAllColumns(self):
		while len(self.c_hLayCol) > 0:
			self.removeColumn()

	def removeColumn(self):
		w = self.c_hLayCol.pop()
		for i in range(w.count()):
			w.itemAt(i).widget().close()
		w.parent().removeItem(w)
		sip.delete(w)

	def genColsLayout(self):
		for name in self.config.get('cols'):
			self.addColLayout(name)

	def addColLayout(self, name, default=False):
		id = len(self.c_hLayCol)
		if True:
			hLayCol         = QtWidgets.QHBoxLayout()
			hLayCol.setObjectName("hLayCol_"+str(id))
			labelCol        = QtWidgets.QLabel(self)
			labelCol.setObjectName("labelCol_"+str(id))
			hLayCol.addWidget(labelCol)
			colName         = QtWidgets.QLineEdit(self)
			colName.setText(name)
			colName.setObjectName("lineEditCol_"+str(id))
			hLayCol.addWidget(colName)
			radioDef        = QtWidgets.QRadioButton(self)
			radioDef.setObjectName("radioDef_"+str(id))
			if self.config.get('default')==id:
				radioDef.setChecked(True)
			else:
				radioDef.setChecked(False)
			hLayCol.addWidget(radioDef)
			labelCol.setText("Col "+str(id)+" :")
			radioDef.setText("Def")
			self.vLayCols.addLayout(hLayCol)

			hLayCol.colName  = colName
			hLayCol.radioDef = radioDef
			self.c_hLayCol.append(hLayCol)
