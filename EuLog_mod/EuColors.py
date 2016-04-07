import json, os

class EuColors:
	def __init__(self):
		self.configuration = {
				'colors'  : [
					{'enabled':True, 'color':'#FF0000', 'regex':'BROKE'},
					{'enabled':True, 'color':'#00FF00', 'regex':'6543' },
					{'enabled':True, 'color':'#0000FF', 'regex':'12345'}]
			}

	def get(self, key):
		return self.configuration[key]

	def set(self, key, value):
		self.configuration[key] = value

	def loadConfig(self, filename):
		if os.path.isfile(filename) :
			with open(filename) as data_file:
				self.configuration = json.load(data_file)

	def writeConfig(self, filename):
		with open(filename, 'wb') as configfile:
			json.dump(self.configuration, configfile)

