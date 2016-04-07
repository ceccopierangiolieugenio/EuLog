import re
from PyQt5.QtCore import Qt, QAbstractTableModel
from PyQt5.QtCore import QModelIndex, QVariant

class EuDataModel(QAbstractTableModel):
	def __init__(self, fileb, config):
		QAbstractTableModel.__init__(self)
		self.fileb = fileb
		self.cols = config.get('cols')
		self.regex = re.compile(config.get('regex'))
		self.default = config.get('default')

	def rowCount(self, parent):
		return self.fileb.getLen()

	def columnCount(self, parent):
		return len(self.cols)

	def data(self, index, role):
		if not index.isValid():
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
	def __init__(self, fileb, config):
		EuDataModel.__init__(self, fileb, config)
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

