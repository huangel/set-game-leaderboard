import time
import os
import sys
import threading

from pynput.keyboard import Key, Controller

import termios
import struct
import fcntl

from timeApp import TimeApp
from card import Card
from deck import Deck
from instructions import Instructions
from leaderboard import Leaderboard

def set_winsize(fd, row, col, xpix=0, ypix=0):
	"""
	Resizes the terminal/console window
	"""
	winsize = struct.pack("HHHH", row, col, xpix, ypix)
	fcntl.ioctl(fd, termios.TIOCSWINSZ, winsize)


class Game:

	def __init__(self, game_length = 30):
		self.score = 0
		self.current_cards = None
		self.start_time = time.time()
		self.game_length = game_length
		self.deck = Deck()
		self.instructions = Instructions() 
		self.leaderboard = Leaderboard()
		self.current_cards = self.deck.get_cards(12)
		self.main_thread = threading.Thread(target=self.main, args=())
		self.main_thread.daemon = True
		self.timer_app = None
		self.high_score = self.leaderboard.get_high_score()
		self.main_thread_active = True

	def start(self):
		# resize terminal
		sys.stdout.write("\x1b[8;{rows};{cols}t".format(rows=40, cols=80))
		self.instructions.display_banner()
		self.instructions.get_instructions()
		start = self.instructions.start_input()

		if start == "Y":
			keyboard = Controller()
			self.main_thread.start()
			self.start_timer()
			keyboard.press(Key.enter)
			keyboard.release(Key.enter)		
			self.end_game()

			self.instructions.end_of_game(self.score)
			high_scores = self.leaderboard.get_high_score()

			if high_scores == (None, None):
				self.instructions.new_high_score("No One :)", 0)
			elif self.score > self.high_score[1]:
				self.instructions.new_high_score(high_scores[0], high_scores[1])
			else:
				self.instructions.old_high_score(high_scores[0], high_scores[1])

			name = self.instructions.ask_for_name() 
			self.leaderboard.set_score(name, self.score)
			return
			
		elif start == "N":
			return

		elif start == "L":
			self.instructions.display_leaderboard(self.leaderboard.get_leaderboard())
			menu = self.instructions.main_menu()
			if menu == "Y":
				self.start()
			return
		else: 
			self.instructions.enter_valid_choice()
			self.start()

	def start_timer(self):
		self.timer_app = TimeApp(self.game_length, self)
		self.timer_app.mainloop()

	def end_game(self):
		self.main_thread_active = False
		try:
			self.timer_app.destroy()
		except:
			pass
		self.main_thread.join(1)
		
	def main(self):
		while self.main_thread_active:
			self.instructions.display_game(self.current_cards, self.score)
			if len(self.current_cards) < 3:
				self.instructions.finish_game()
				break
			else:
				value = self.instructions.ask_for_cards()

				try:
					if value.strip().upper() == 'A':
						self.current_cards.extend(self.deck.get_cards(3))
						continue

					else:
						x, y, z = value.split()
						x = int(x)
						y = int(y)
						z = int(z)
				except:
					self.instructions.wrong_input()
					continue					

				if (x > len(self.current_cards) or x < 0 or y > len(self.current_cards) or y < 0 or z > len(self.current_cards) or z < 0):
					self.instructions.wrong_index()
					continue

				if self.is_set(x, y, z) and len(self.current_cards) > 12: #check if the inputs make a set 
					self.score +=1
					self.remove_cards([x, y, z])

				elif self.is_set(x, y, z):
					if len(self.deck.available_cards) > 2:
						self.current_cards[x] = self.deck.get_cards(1)[0] #replace card x 
						self.current_cards[y] = self.deck.get_cards(1)[0]
						self.current_cards[z] = self.deck.get_cards(1)[0]
						self.score += 1
					else:
						self.remove_cards([x, y, z])
						self.score += 1

				else:
					self.instructions.wrong_set()

	def is_set(self, x, y, z):
		x = int(x)
		y = int(y)
		z = int(z)
		val = False
		val_x = self.current_cards[x].value
		val_y = self.current_cards[y].value
		val_z = self.current_cards[z].value

		size = False
		size_x = self.current_cards[x].size
		size_y = self.current_cards[y].size
		size_z = self.current_cards[z].size

		shape = False
		shape_x = self.current_cards[x].shape
		shape_y = self.current_cards[y].shape
		shape_z = self.current_cards[z].shape

		if (val_x == val_y == val_z) or (val_x != val_y != val_z):
			val = True
		if (size_x == size_y == size_z) or (size_x != size_y != size_z):
			size = True
		if (shape_x == shape_y == shape_z) or (shape_x != shape_y != shape_z):
			shape = True

		if val and size and shape:
			return True

	def remove_cards(self, indicies):
		new = []
		for i, ele in enumerate(self.current_cards):
			if i not in indicies:
				new.append(ele)
		self.current_cards = new

if __name__ == '__main__':
	s = Game()
	start = s.start()