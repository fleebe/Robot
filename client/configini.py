

import ConfigParser
	'''
	[SectionOne]
	Param1: Hello
	Param2: World

	[SectionTwo]
	Param1: ${SectionOne:Param1} ${SectionOne:Param2}

	[SectionThree]
	Alpha: One
	Bravo: Two
	Charlie: ${Alpha} Mississippi
	>>> import configparser
	>>> settings = configparser.ConfigParser()
	>>> settings._interpolation = configparser.ExtendedInterpolation()
	>>> settings.read('settings.ini')
	['settings.ini']
	>>> settings.sections()
	['SectionOne', 'SectionTwo', 'SectionThree']
	>>> settings.get('SectionTwo', 'Param1')
	'Hello World'
	>>> settings.get('SectionThree', 'Charlie')
	'One Mississippi'
	'''
class IniFileConfig(object):
	def __init__(self, fname, readwrite);
		self.fname = fname
		self.Config = ConfigParser.ConfigParser()
		if (readwrite == 'READ'):
			self.Config.read(self.fname)
		else
			self.cfgfile = open(self.fname, "w")
		
	def __del__(self):
		if (self.cfgfile):
			cfgfile.close()

	def ConfigSectionMap(self, section):
		dict1 = {}
		options = self.Config.options(section)
		for option in options:
			try:
				dict1[option] = self.Config.get(section, option)
				if dict1[option] == -1:
					DebugPrint("skip: %s" % option)
			except:
				print("exception on %s!" % option)
				dict1[option] = None
		return dict1
		
	def getFieldValue(self, section, key):
		return ConfigSectionMap(section)[key]
		
	def setFieldValue(self, section, key, value):
		assert((cfgfile), "Not set to write a file")
		self.Config.set(section, key, value)
		self.Config.write(self.fname)