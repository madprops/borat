# Modules
from configuration import config
import utils

# Standard
import re
import random
from typing import List, Any

def check_random() -> None:
	if not config.words:
		return

	def replace(match: re.Match[Any]) -> str:
		number = 1

		if match["number"]:
			numrange = utils.extract_range(match["number"])

			if len(numrange) == 1:
				if numrange[0] > 0:
					number = numrange[0]
			elif len(numrange) > 1:
				if numrange[0] < numrange[1]:
					number = random.randint(numrange[0], numrange[1])

		randwords: List[str] = []

		for _ in range(number):
			allow_zero = True

			if number > 1:
				if len(randwords) == 0:
					allow_zero = False

			randwords.append(get_random(match["word"], allow_zero))

		if match["word"] == "number":
			return "".join(randwords)
		else:
			return " ".join(randwords)

	new_lines: List[str] = []
	pattern = re.compile(r"\[(?P<word>random|number)(?:\s+(?P<number>\d+(-\d+)?))?\]", re.IGNORECASE)
	pattern_multi = re.compile(r"\[(?:x(?P<number>\d+))?\]$", re.IGNORECASE)

	for line in config.words:
		match = re.search(pattern, line)

		if match:
			multi = 1
			match_multi = re.search(pattern_multi, line)

			if match_multi:
				multi = max(1, int(match_multi["number"]))
				line = re.sub(pattern_multi, "", line)

			for _ in range(multi):
				new_line = re.sub(pattern, replace, line)
				new_lines.append(new_line)
		else:
			new_lines.append(line)

	config.words = new_lines

def check_repeat() -> None:
	if not config.words:
		return

	new_lines: List[str] = []
	pattern = re.compile(r"^\[(?P<word>repeat)(?:\s+(?P<number>\d+))?\]$", re.IGNORECASE)

	for line in config.words:
		match = re.match(pattern, line)

		if match:
			num = match["number"]
			number = int(num) if num is not None else 1
			new_lines.extend([new_lines[-1]] * number)
		else:
			new_lines.append(line)

	config.words = new_lines

def check_empty() -> None:
	if not config.words:
		return

	new_lines: List[str] = []
	pattern = re.compile(r"^\[(?P<word>empty)(?:\s+(?P<number>\d+))?\]$", re.IGNORECASE)

	for line in config.words:
		match = re.match(pattern, line)

		if match:
			num = match["number"]
			number = int(num) if num is not None else 1

			for _ in range(number):
				new_lines.append("")
		else:
			new_lines.append(line)

	config.words = new_lines

def random_word() -> str:
	if not config.randomlist:
		lines = config.randomfile.read_text().splitlines()
		config.randomlist = [line.strip() for line in lines]

	if not config.randwords:
		config.randwords = config.randomlist.copy()

	if not config.randwords:
		return ""

	w = random.choice(config.randwords)

	if not config.repeatrandom:
		config.randwords.remove(w)

	return w

def get_random(rand: str, allow_zero: bool) -> str:
	if rand == "random":
		return random_word().lower()
	elif rand == "RANDOM":
		return random_word().upper()
	elif rand == "Random":
		return random_word().title()
	elif rand == "number":
		return str(utils.random_digit(allow_zero))
	else:
		return ""