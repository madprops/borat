# Modules
from config import Global
import words

# Standard
import re
import random

def check_random():
	if len(Global.words) == 0:
		return

	new_words = []

	for word in Global.words:
		pattern = re.compile(r"\[(?P<word>random)(?:\s+(?P<number>\d+))?\]", re.IGNORECASE)
		match = re.match(pattern, word)

		if match:
			n = match["number"]
			number = int(n) if n is not None else 1
			rand = match["word"]
			randwords = []

			for _ in range(number):
				if rand == "random":
					randwords.append(words.random_word().lower())
				elif rand == "RANDOM":
					randwords.append(words.random_word().upper())
				elif rand == "Random":
					randwords.append(words.random_word().title())

			new_words.append(" ".join(randwords))
		else:
			new_words.append(word)

	Global.words = new_words

def check_repeat():
	if len(Global.words) == 0:
		return

	new_words = []

	for word in Global.words:
		pattern = re.compile(r"\[(?P<word>repeat)(?:\s+(?P<number>\d+))?\]", re.IGNORECASE)
		match = re.match(pattern, word)

		if match:
			n = match["number"]
			number = int(n) if n is not None else 1
			new_words.extend([Global.words[Global.words.index(word) - 1]] * number)
		else:
			new_words.append(word)

	Global.words = new_words

def random_word():
	if len(Global.wordlist) == 0:
		with open(Global.wordfile, "r") as file:
			lines = file.readlines()
			Global.wordlist = [item.strip() for line in lines for item in line.split() if item.strip()]

	return random.choice(Global.wordlist)