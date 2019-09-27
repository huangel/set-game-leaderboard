import random
from card import Card

class Deck:
	def __init__(self):
		self.available_cards = self.generate_cards()

	def get_cards(self, n):
		"""	
			pops n cards off the deck, and returns them in a list
			returns None if no cards left.
		"""
		popped_cards = []
		for i in range(n):
			popped_cards.append(self.available_cards.pop())
		return popped_cards

	def generate_cards(self):
		"""
			Generates a list of all possible cards, randomly shuffled
		"""
		full_deck = []
		for num in range(0, 3): #0, 1, 2 for value
			for size in range(1, 4): # 1, 2,3 for size
				for shape in ['tuple', 'list', 'set']:
					full_deck.append(Card(num, size, shape))
		random.shuffle(full_deck)
		return full_deck