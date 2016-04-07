import sip, os

from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt, QVariant
from PyQt5.QtWidgets import *

qtCreatorFile = 'ui/EuLog.Colors.ui'

Ui_ConfigDiag, QtBaseClass = uic.loadUiType(qtCreatorFile)

class EuColorsDialog(QDialog, Ui_ConfigDiag):
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
		self.colorsComboBox.insertItem(1, 'default.cfg')
		for files in os.listdir('colors'):
			if files != 'default.cfg':
				self.colorsComboBox.insertItem(1, files)

		self.c_hLayCol = []
		self.setConfig()

		self.addColumnButton.clicked.connect(self.addColumn)
		self.removeColumnButton.clicked.connect(self.removeColumn)
		self.okButton.clicked.connect(self.saveAndClose)
		self.newProfileButton.clicked.connect(self.newProfile)
		self.colorsComboBox.currentIndexChanged.connect(self.profileChanged)

		QtCore.QMetaObject.connectSlotsByName(self)

	def newProfile(self):
		name, ok = QInputDialog.getText(self, 'New Profile', 'New profile name:')
		if ok:
			self.config.writeConfig(os.path.join('colors', name))
			self.colorsComboBox.insertItem(1, name)
			self.colorsComboBox.setCurrentIndex(1)

	def saveAndClose(self):
		profile = self.colorsComboBox.currentText()
		colors = []
		for color in self.c_hLayCol:
			colors.append({
					'enabled':color.checkEnable.isChecked(),
					'color':color.colorButton.color(),
					'regex':color.colorRegex.text()
				})
		self.config.set('colors',colors)
		self.config.writeConfig(os.path.join('colors','default.cfg'))
		self.config.writeConfig(os.path.join('colors',profile))
		self.close()

	def setConfig(self):
		self.removeAllColumns()
		self.genColsLayout()

	def profileChanged(self, val):
		profile = self.colorsComboBox.itemText(val)
		self.config.loadConfig(os.path.join('colors',profile))
		self.setConfig()

	def addColumn(self):
		self.addColLayout({'enabled':False, 'color':'#FFFFFF', 'regex':''})

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
		for name in self.config.get('colors'):
			self.addColLayout(name)

	def addColLayout(self, color):
		id = len(self.c_hLayCol)
		if True:
			hLayCol = QtWidgets.QHBoxLayout()
			colorButton = QColorButton()
			hLayCol.addWidget(colorButton)
			colorButton.setColor(color['color'])
			colorRegex = QtWidgets.QLineEdit(self)
			colorRegex.setText(color['regex'])
			hLayCol.addWidget(colorRegex)
			checkEnable = QtWidgets.QCheckBox(self)
			checkEnable.setChecked(color['enabled'])
			hLayCol.addWidget(checkEnable)
			checkEnable.setText("Def")
			self.vLayColors.addLayout(hLayCol)

			hLayCol.colorRegex    = colorRegex
			hLayCol.checkEnable = checkEnable
			hLayCol.colorButton = colorButton
			self.c_hLayCol.append(hLayCol)


# Color picker by Martin Fitzpatrick (https://github.com/mfitzp)
# http://martinfitzpatrick.name/article/qcolorbutton-a-color-selector-tool-for-pyqt/

class QColorButton(QPushButton):
	'''
	Custom Qt Widget to show a chosen color.

	Left-clicking the button shows the color-chooser, while
	right-clicking resets the color to None (no-color).	
	'''

	def __init__(self, *args, **kwargs):
		super(QColorButton, self).__init__(*args, **kwargs)

		self._color = None
		self.setMaximumWidth(32)
		self.pressed.connect(self.onColorPicker)

	def setColor(self, color):
		if color != self._color:
			self._color = color
		if self._color:
			self.setStyleSheet("background-color: %s;" % self._color)
		else:
			self.setStyleSheet("")

	def color(self):
		return self._color

	def onColorPicker(self):
		'''
		Show color-picker dialog to select color.

		Qt will use the native dialog by default.

		'''
		dlg = QColorDialog(QColor(self._color))
		if self._color:
			dlg.setCurrentColor(QColor(self._color))

		if dlg.exec_():
			self.setColor(dlg.currentColor().name())

	def mousePressEvent(self, e):
		if e.button() == Qt.RightButton:
			self.setColor(None)

		return super(QColorButton, self).mousePressEvent(e)

