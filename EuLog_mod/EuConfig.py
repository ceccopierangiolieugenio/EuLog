import ConfigParser

class EuConfig:
	def __init__(self):
		self.configuration = {
				'regex'   : '(.*)',
				'cols'    : ['TXT'],
				'default' : 0
			}

	def get(self, key):
		return self.configuration[key]

	def set(self, key, value):
		self.configuration[key] = value

	def loadConfig(self, filename):
		config = ConfigParser.RawConfigParser()
		config.read(filename)
		self.configuration['regex']   = config.get('Parser','regex')
		self.configuration['cols']    = config.get('Parser','cols').split(';')
		self.configuration['default'] = int(config.get('Parser','default'))
		return

	def writeConfig(self, filename):
		config = ConfigParser.RawConfigParser()

		config.add_section('Parser')
		config.set('Parser', 'regex', self.configuration['regex'])
		config.set('Parser', 'cols', ';'.join(self.configuration['cols']))
		config.set('Parser', 'default', self.configuration['default'])

		# Writing our configuration file to 'example.cfg'
		with open(filename, 'wb') as configfile:
			    config.write(configfile)
