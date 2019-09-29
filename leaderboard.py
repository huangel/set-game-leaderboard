import os

class Leaderboard():

	def __init__(self):
		self.file = ".setgame"
		self.high_score_name = None
		self.high_score = None
		self.scores = {}
		self._get_leaderboard_score_init()

	def set_score(self, name, score):
		with open(self.file, 'a') as f:
			f.write(str(name) + "," + str(score) + "\n")
		self._check_high_score(name, score)
		self._insert_score_into_dic(name, score)

	def get_leaderboard(self):
		return sorted(self.scores.items(), key = lambda x:x[1], reverse = True)

	def get_high_score(self):
		return self.high_score_name, self.high_score

	def clear_leaderboard(self):
		os.remove(self.file)
		self.scores = {}
		self.high_score_name = None
		self.high_score = None 

	def _get_leaderboard_score_init(self):
		exists = os.path.isfile(self.file)
		high_score = -1
		name = None
		if exists:
			for line in open(self.file, 'r'):
				line = line.rstrip().split(",")
				cur_name, cur_score = line[0], int(line[1])
				self._check_high_score(cur_name, cur_score)
				self._insert_score_into_dic(cur_name, cur_score)

	def _check_high_score(self, cur_name, cur_score):
		if self.high_score is None:
			self.high_score = cur_score
			self.high_score_name = cur_name
		if cur_score > self.high_score:
			self.high_score = cur_score 
			self.high_score_name = cur_name

	def _insert_score_into_dic(self, cur_name, cur_score):
		if cur_name in self.scores:
			if cur_score > self.scores[cur_name]:
				self.scores[cur_name] = cur_score
		else:
			self.scores[cur_name] = cur_score 