import sip, os

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QVariant
from PyQt5.QtWidgets import *


class EuConfigDialog(QDialog):
	def __init__(self, config):
		self.config = config
		QDialog.__init__(self)
		self.setWindowModality(Qt.ApplicationModal)
		self.initUI()
		self.show()

	def initUI(self):
		self.setWindowTitle('Preferences')
		self.resize(800,500)
		self.verticalLayout = QtWidgets.QVBoxLayout(self)
		self.verticalLayout.setObjectName("verticalLayout")
		self.hLayProfile = QtWidgets.QHBoxLayout()
		self.hLayProfile.setObjectName("hLayProfile")
		self.label_4 = QtWidgets.QLabel(self)
		self.label_4.setMaximumSize(QtCore.QSize(80, 16777215))
		self.label_4.setObjectName("label_4")
		self.label_4.setText("Profile")
		self.hLayProfile.addWidget(self.label_4)
		self.profilesComboBox = QtWidgets.QComboBox(self)
		self.profilesComboBox.setObjectName("comboBox")
		self.hLayProfile.addWidget(self.profilesComboBox)
		self.verticalLayout.addLayout(self.hLayProfile)
		self.hLayRegex = QtWidgets.QHBoxLayout()
		self.hLayRegex.setObjectName("hLayRegex")
		self.label = QtWidgets.QLabel(self)
		self.label.setObjectName("label")
		self.label.setText("Regex:")
		self.hLayRegex.addWidget(self.label)
		self.lineEditRegex = QtWidgets.QLineEdit(self)
		self.lineEditRegex.setObjectName("lineEditRegex")
		self.hLayRegex.addWidget(self.lineEditRegex)
		self.verticalLayout.addLayout(self.hLayRegex)

		self.hLayCtl = QtWidgets.QHBoxLayout()
		self.hLayCtl.setObjectName("hLayCtl")
		self.addColumnButton = QtWidgets.QPushButton(self)
		self.addColumnButton.setObjectName("addColumnButton")
		self.addColumnButton.setText("Add Column")
		self.hLayCtl.addWidget(self.addColumnButton)
		self.removeColumnButton = QtWidgets.QPushButton(self)
		self.removeColumnButton.setObjectName("removeColumnButton")
		self.removeColumnButton.setText("Remove Column")
		self.hLayCtl.addWidget(self.removeColumnButton)
		spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
		self.hLayCtl.addItem(spacerItem)
		self.verticalLayout.addLayout(self.hLayCtl)

		self.vLayCols = QtWidgets.QVBoxLayout()
		self.verticalLayout.addLayout(self.vLayCols)

		spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
		self.verticalLayout.addItem(spacerItem1)
		self.hLayOkCancel = QtWidgets.QHBoxLayout()
		self.hLayOkCancel.setObjectName("hLayOkCancel")
		spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
		self.hLayOkCancel.addItem(spacerItem2)
		self.okButton = QtWidgets.QPushButton(self)
		self.okButton.setObjectName("okButton")
		self.hLayOkCancel.addWidget(self.okButton)
		self.cancelButton = QtWidgets.QPushButton(self)
		self.cancelButton.setObjectName("cancelButton")
		self.hLayOkCancel.addWidget(self.cancelButton)
		self.verticalLayout.addLayout(self.hLayOkCancel)
		self.okButton.setText("OK")
		self.cancelButton.setText("Cancel")

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
		self.cancelButton.clicked.connect(self.close)
		self.profilesComboBox.currentIndexChanged.connect(self.profileChanged)

		QtCore.QMetaObject.connectSlotsByName(self)

	def saveAndClose(self):
		profile = self.profilesComboBox.currentText()
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
			#removeColButton = QtWidgets.QPushButton(self)
			#removeColButton.setObjectName("removeColButton_"+str(id))
			#removeColButton.setText("X")
			#removeColButton.setMaximumSize(QtCore.QSize(32, 16777215))
			#hLayCol.addWidget(removeColButton)
			labelCol        = QtWidgets.QLabel(self)
			labelCol.setObjectName("labelCol_"+str(id))
			hLayCol.addWidget(labelCol)
			colName         = QtWidgets.QLineEdit(self)
			colName.setText(name)
			colName.setObjectName("lineEditCol_"+str(id))
			hLayCol.addWidget(colName)
			radioDef        = QtWidgets.QRadioButton(self)
			radioDef.setObjectName("radioDef_"+str(id))
			hLayCol.addWidget(radioDef)
			labelCol.setText("Col "+str(id)+" :")
			radioDef.setText("Def")
			self.vLayCols.addLayout(hLayCol)

			self.c_hLayCol.append(hLayCol)
