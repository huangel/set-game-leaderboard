class Card:
	
	def __init__(self, value, size, shape):
		self.value = value
		self.size = size
		self.shape = shape

	def __str__(self):
		output = str(self.value)*self.size

		if self.shape == 'tuple':
			return '(' + output + ')'
		elif self.shape == 'list':
			return '[' + output + ']'
		elif self.shape == 'set':
			return '{' + output + '}'
		else:
			return None
