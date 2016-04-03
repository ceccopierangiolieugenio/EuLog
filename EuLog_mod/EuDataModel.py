import re
from PyQt5.QtCore import Qt, QAbstractTableModel, QVariant

class EuDataModel(QAbstractTableModel):
	def __init__(self, fileb, regex, cols):
		QAbstractTableModel.__init__(self)
		self.fileb = fileb
		self.cols = cols
		self.regex = re.compile(regex)

	def rowCount(self, parent): 
		return self.fileb.GetLen()
 
	def columnCount(self, parent): 
		return len(self.cols) 
 
	def data(self, index, role): 
		if not index.isValid(): 
			return QVariant() 
		elif role != Qt.DisplayRole: 
			return QVariant() 
		m = self.regex.match(self.fileb.GetLine(index.row()))
		if m:
			return m.group(1+index.column())
		else:
			return "Error"

	def headerData(self, col, orientation, role):
		if orientation == Qt.Horizontal and role == Qt.DisplayRole:
			return QVariant(self.cols[col])

class EuDataModelSearch(EuDataModel):
	def __init__(self, fileb, regex, cols, indexes):
		EuDataModel.__init__(self, fileb, regex, cols)
		self.indexes = indexes;

	def rowCount(self, parent): 
		return len(self.indexes)
 
	def data(self, index, role):
		if not index.isValid(): 
			return QVariant() 
		elif role != Qt.DisplayRole: 
			return QVariant() 
		m = self.regex.match(self.fileb.GetLine(self.indexes[index.row()]))
		if m:
			return m.group(1+index.column())
		else:
			return "Error"

