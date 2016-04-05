import re

class EuFileBuf:
	def __init__(self, filename):
		self.filename = filename
		self.indexes = []
		self.createIndex()
		self.fd = open(self.filename,'r')
		self.lastline = {'line':0, 'txt':self.fd.readline()}

	def __del__(self):
		self.fd.close()

	def getLen(self):
		return len(self.indexes)

	def getLine(self, line):
		if line >= self.getLen():
			return ""
		if self.lastline['line'] != line :
			self.fd.seek(self.indexes[line])
			self.lastline = {'line':line, 'txt':self.fd.readline()}
		return self.lastline['txt']


	def createIndex(self):
		self.indexes = []
		lines = 0
		offset = 0
		with open(self.filename,'r') as infile:
			for line in infile:
				lines += 1
				self.indexes.append(offset)
				offset += len(line)

	def search(self, regex):
		indexes = []
		id = 0
		rr = re.compile(regex)
		with open(self.filename,'r') as infile:
			for line in infile:
				ma = rr.match(line)
				if ma:
					indexes.append(id)
				id += 1
		return indexes
		

