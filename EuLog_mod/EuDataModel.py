import re
from PyQt5.QtCore import Qt, QAbstractTableModel
from PyQt5.QtCore import QModelIndex, QVariant

class EuDataModel(QAbstractTableModel):
	def __init__(self, fileb, regex, cols):
		QAbstractTableModel.__init__(self)
		self.fileb = fileb
		self.cols = cols
		self.regex = re.compile(regex)

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
		m = self.regex.match(self.fileb.getLine(row))
		if m:
			return m.group(1+col)
		else:
			return "Error"

	def headerData(self, col, orientation, role):
		if orientation == Qt.Vertical and role == Qt.DisplayRole:
			return QVariant(col)
		if orientation == Qt.Horizontal and role == Qt.DisplayRole:
			return QVariant(self.cols[col])

class  EuDataProxyModel(EuDataModel):
	def __init__(self, fileb, regex, cols):
		EuDataModel.__init__(self, fileb, regex, cols)
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

