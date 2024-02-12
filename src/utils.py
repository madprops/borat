# Standard
import sys
import random
import string
import tomllib
from pathlib import Path

def random_string():
	vowels = "aeiou"
	consonants = "".join(set(string.ascii_lowercase) - set(vowels))

	def con():
		return random.choice(consonants)

	def vow():
		return random.choice(vowels)

	return con() + vow() + con() + vow() + con() + vow()

def get_extension(path):
	return Path(path).suffix.lower()

def resolve_path(path):
	pth = Path(path).expanduser()

	if pth.is_absolute():
		return full_path(pth)
	else:
		return full_path(Path(Path.cwd(), pth))

def full_path(path):
	return path.expanduser().resolve()

def exit(message):
	print(f"\nExit: {message}\n")
	sys.exit(0)

def read_toml(path):
	with open(path, "rb") as file:
		return tomllib.load(file)