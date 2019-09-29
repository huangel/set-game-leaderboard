import os
import sys
import time

class Instructions:
	def __init__(self):
		pass

	def display_banner(self):
    # Clears the terminal screen, and displays a title bar.
	    os.system('cls' if os.name == 'nt' else 'clear') #cls for window and clear for Linux/Mac
	              
	    print("\t**********************************************")
	    print("\t***              Game of SET               ***")
	    print("\t**********************************************")

	def get_instructions(self):
		print("Welcome to SET!\n")
		print("There are five basic rules.\n")
		print("1. Identify as many SETs as possible in the given time.")
		print("2. There are three features - shape (the type of the card), value (the number in the card, and size (the length of the card).")
		print("3. A SET consists three cards in which each feature is either the same on each card or is different on each card.")
		print("4. If you find a SET, enter the indexes of the three cards, separating each index with a space.")
		print("5. If you can't find a SET in the given 12 cards, enter A for the dealer to generate three additional cards.\n")

	def start_input(self):
		return input("Do you want to start the game [Y], look at leadership board [L], or exit [N]? [Y/L/N] ").upper()

	def main_menu(self):
		return input("Do you want to return to the main menu? [Y/N] ").upper()

	def new_high_score(self, name, score):
		print("New high score! You beat {}'s high score of {}".format(name, score))

	def old_high_score(self, name, score): 
		print("{} has the high score of {}".format(name, score))

	def finish_game(self):
		print("Congrats! You've finished the game.")

	def ask_for_cards(self):
		print('What three cards make a SET?')
		return sys.stdin.readline()

	def ask_for_name(self):
		print("What is your name? ")
		return sys.stdin.readline().strip()

	def end_of_game(self, score):
		print('\nEnd of Game! Your score is', score)

	def wrong_input(self):
		print("Please enter three integers (i.e. `2 4 5`) or `A` to add 3 cards")
		time.sleep(1.5)

	def wrong_index(self):
		print("Please enter the index of the cards")
		time.sleep(1.5)

	def wrong_set(self):
		sys.stdout.write("\r")
		sys.stdout.write("Sorry! That's not a SET.")
		sys.stdout.flush()
		time.sleep(1.5)

	def enter_valid_choice(self):
		print("Please enter a valid choice.")
		time.sleep(1)

	def display_game(self, cards, score):
		"""
		outputs to the user the cards in self.current_cards
		"""
		os.system('cls' if os.name == 'nt' else 'clear')
		self.display_banner()
		print('Score', score)
		current = [str(i) for i in cards]
		print('--------------')
		for i in range(len(current)):
			print('{:^{}}'.format(i, 4) + '* {:^{}} *'.format(current[i], 5))
			print('--------------')

	def display_leaderboard(self, scores):
		ranks = len(str(len(scores)))
		longest_name = len(sorted(scores, key = lambda x : len(x[0]), reverse = True)[0][0])
		longest_score = len(str(scores[0][1]))

		title = "   rank   |   name   |   score   "
		if ranks < 4:
			ranks = 4 
		if longest_name < 4:
			longest_name = 4
		if longest_score < 5:
			longest_score = 5

		print("   Rank" + " "*(ranks-4) + "   " + \
			  "|   Name" + " "*(longest_name - 4)  + "   " + \
			  "|   Score" + " "*(longest_score - 5) + "   ")

		print("-" * (ranks + longest_name + longest_score + 18))
		for order, (name, score) in enumerate(scores):
			order_len = len(str(order+1))
			name_len = len(name)
			score_len = len(str(score))

			print("   {}".format(order+1) + " "*(ranks-order_len) + "   " + \
				  "|   {}".format(name) + " "*(longest_name - name_len)  + "   " + \
				  "|   {}".format(score) + " "*(longest_score - score_len) + "   ")

			print("-" * (ranks + longest_name + longest_score + 18))