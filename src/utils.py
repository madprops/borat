# Standard
import re
import sys
import random
import string
import colorsys
from pathlib import Path
from typing import List, Dict, Union

def random_string() -> str:
	vowels = "aeiou"
	consonants = "".join(set(string.ascii_lowercase) - set(vowels))

	def con() -> str:
		return random.choice(consonants)

	def vow() -> str:
		return random.choice(vowels)

	return con() + vow() + con() + vow() + con() + vow()

def get_extension(path: Path) -> str:
	return Path(path).suffix.lower().lstrip(".")

def resolve_path(path: Path) -> Path:
	pth = Path(path).expanduser()

	if pth.is_absolute():
		return full_path(pth)
	else:
		return full_path(Path(Path.cwd(), pth))

def full_path(path: Path) -> Path:
	return path.expanduser().resolve()

def exit(message: str) -> None:
	print(f"\nExit: {message}\n")
	sys.exit(1)

def read_toml(path: Path) -> Union[Dict[str, str], None]:
	import tomllib

	if (not path.exists()) or (not path.is_file()):
		exit("TOML file does not exist")
		return None

	try:
		return tomllib.load(open(path, "rb"))
	except Exception as e:
		print(f"Error: {e}")
		exit("Failed to read TOML file")
		return None

def random_color(lightness: float) -> List[int]:
	hue = random.random()
	saturation = 0.8
	r, g, b = colorsys.hsv_to_rgb(hue, saturation, lightness)
	r, g, b = int(r * 255), int(g * 255), int(b * 255)
	return [r, g, b]

def random_light() -> List[int]:
	return random_color(0.8)

def random_dark() -> List[int]:
	return random_color(0.2)

def random_digit(allow_zero: bool) -> int:
	if allow_zero:
		return random.randint(0, 9)
	else:
		return random.randint(1, 9)

def extract_range(string: str) -> List[int]:
	pattern = re.compile(r"(\d+)(?:-(\d+))?")
	match = pattern.search(string)

	if not match:
		return [0]

	start = match.group(1)
	end = match.group(2)

	if end is None:
		return [int(start)]
	else:
		return [int(start), int(end)]