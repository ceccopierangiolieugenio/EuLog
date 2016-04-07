import re
from PyQt5.QtGui  import QColor, QBrush
from PyQt5.QtCore import Qt, QAbstractTableModel
from PyQt5.QtCore import QModelIndex, QVariant

class EuDataModel(QAbstractTableModel):
	def __init__(self, fileb, config, colors):
		QAbstractTableModel.__init__(self)
		self.fileb = fileb
		self.config = config
		self.c_conf = colors
		self.updateConfig()

	def updateConfig(self):
		self.beginResetModel()
		self.cols = self.config.get('cols')
		self.regex = re.compile(self.config.get('regex'))
		self.default = self.config.get('default')
		self.colors  = self.c_conf.get('colors')
		self.endResetModel()

	def rowCount(self, parent):
		return self.fileb.getLen()

	def columnCount(self, parent):
		return len(self.cols)

	def data(self, index, role):
		if not index.isValid():
			return QVariant()
		elif role == Qt.BackgroundRole:
			line = self.fileb.getLine(index.row())
			for color in self.colors:
				if color['enabled']:
					m = re.search('.*'+color['regex'],line)
					if m: return QBrush(QColor(color['color']))
			return QVariant()
		elif role != Qt.DisplayRole:
			return QVariant()
		return self.euGet(index.row(),index.column())

	def euGet(self, row, col):
		line = self.fileb.getLine(row)
		m = self.regex.match(line)
		if m:
			return m.group(1+col)
		if self.default==col:
			return line
		return ""

	def headerData(self, col, orientation, role):
		if orientation == Qt.Vertical and role == Qt.DisplayRole:
			return QVariant(col)
		if orientation == Qt.Horizontal and role == Qt.DisplayRole:
			return QVariant(self.cols[col])

class  EuDataProxyModel(EuDataModel):
	def __init__(self, fileb, config, colors):
		EuDataModel.__init__(self, fileb, config, colors)
		self.indexes = []

	def euSetIndexes(self, indexes):
		self.beginResetModel()
		self.indexes = indexes
		self.endResetModel()

	def rowCount(self, parent):
		return len(self.indexes)

	def data(self, index, role):
		if not index.isValid():
			return QVariant()
		elif role != Qt.DisplayRole:
			return QVariant()
		return self.euGet(self.indexes[index.row()],index.column())

	def headerData(self, col, orientation, role):
		if orientation == Qt.Vertical and role == Qt.DisplayRole:
			return self.indexes[col];
		return EuDataModel.headerData(self, col, orientation, role)

