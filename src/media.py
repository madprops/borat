# Modules
from configuration import config
import utils

# Libraries
import cv2 # type: ignore
from PIL import Image # type: ignore

# Standard
from pathlib import Path
import random
from typing import List, Any, Dict, Tuple, Union

def get_frames(path: Path) -> List[Any]:
	frames = []
	ext = utils.get_extension(path)

	if ext == ".jpg" or ext == ".png":
		assert isinstance(config.frames, int)

		for _ in range(0, config.frames):
			frame = cv2.imread(str(path))
			frames.append(frame)
	else:
		cap = cv2.VideoCapture(str(path))
		total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
		assert isinstance(config.frames, int)
		num_frames = total_frames if config.remake else config.frames
		order = "normal" if (config.remake or config.framelist) else config.order
		framelist = config.framelist if config.framelist else range(total_frames)
		current = 0

		# Sometimes it fails to read the frames so it needs more tries
		for _ in range(0, num_frames * 25):
			if order == "normal":
				index = framelist[current]
			elif order == "random":
				index = random.choice(framelist)

			cap.set(cv2.CAP_PROP_POS_FRAMES, index)
			ret, frame = cap.read()

			if ret:
				frames.append(frame)

			if len(frames) == num_frames:
				break

			if order == "normal":
				current += 1

				if current >= len(framelist):
					current = 0

		cap.release()

	return frames

def add_text(frame: Any, lines: List[str]) -> Any:
	font = get_font()
	data = get_text_data(frame, lines)
	padding = config.padding

	if config.fontcolor == "random_light2":
		rgb_font = utils.random_light()
	elif config.fontcolor == "random_dark2":
		rgb_font = utils.random_dark()
	elif isinstance(config.fontcolor, list):
		rgb_font = list(reversed((config.fontcolor)))
	else:
		rgb_font = [255, 255, 255]

	if config.bgcolor:
		if config.baseline:
			baseline = data["framedata"][0]["baseline"]
		else:
			baseline = 0

		if config.bgcolor == "random_light2":
			rgb_bg = utils.random_light()
		elif config.bgcolor == "random_dark2":
			rgb_bg = utils.random_dark()
		elif isinstance(config.bgcolor, list):
			rgb_bg = list(reversed((config.bgcolor)))
		else:
			rgb_bg = [0, 0, 0]

		rect_1 = (data["min_x_rect"] - padding, data["min_y_rect"] - padding)
		rect_2 = (data["max_x_rect"] + padding, data["max_y_rect"] + padding + baseline)

		rcopy = cv2.rectangle(frame.copy(), (rect_1), rect_2, rgb_bg, -1)
		cv2.addWeighted(frame, 1 - config.opacity, rcopy, config.opacity, 0, frame)

	for i, line in enumerate(lines):
		framedata = data["framedata"][i]
		position = (framedata["x"], framedata["y"])
		cv2.putText(frame, line, position, font, config.fontsize, rgb_font, config.boldness, cv2.LINE_AA)

	return frame

def get_font() -> Any:
	if config.font == "simple":
		font = cv2.FONT_HERSHEY_SIMPLEX
	elif config.font == "complex":
		font = cv2.FONT_HERSHEY_COMPLEX
	elif config.font == "plain":
		font = cv2.FONT_HERSHEY_PLAIN
	elif config.font == "duplex":
		font = cv2.FONT_HERSHEY_DUPLEX
	elif config.font == "triplex":
		font = cv2.FONT_HERSHEY_TRIPLEX
	else:
		font = cv2.FONT_HERSHEY_SIMPLEX

	return font

def get_text_data(frame: Any, lines: List[str]) -> Dict[str, Any]:
	width, height = get_shape(frame)
	max_width, max_height = 0, 0
	font = get_font()
	lineheight = 0
	framedata = []

	p_top = config.top
	p_bottom = config.bottom
	p_left = config.left
	p_right = config.right
	padding = config.padding

	for line in lines:
		text_size, baseline = cv2.getTextSize(line, font, config.fontsize, config.boldness)
		text_width = text_size[0]
		text_height = text_size[1]
		max_height += text_height + config.linespace

		if text_width > max_width:
			max_width = text_width

		if (p_left is not None) and (p_left >= 0):
			text_x = p_left + padding
		elif (p_right is not None) and (p_right >= 0):
			text_x = width - text_width - p_right - padding
		else:
			text_x = (width - text_width) // 2

			if (p_left is not None) and (p_left < 0):
				text_x += p_left
			elif (p_right is not None) and (p_right < 0):
				text_x -= p_right

		if (p_top is not None) and (p_top >= 0):
			text_y = text_height + p_top + padding
		elif (p_bottom is not None) and (p_bottom >= 0):
			text_y = height - p_bottom - ((len(lines) - 1) * (text_height + config.linespace)) - padding

			if config.baseline:
				text_y -= baseline
		else:
			text_y = (height + text_height) // 2

			if (p_top is not None) and (p_top < 0):
				text_y += p_top
			elif (p_bottom is not None) and (p_bottom < 0):
				text_y -= p_bottom

		text_y += lineheight
		lineheight += text_height + config.linespace
		x_rect = text_x
		y_rect = text_y - text_height

		fdata = {
			"width": text_width,
			"height": text_height,
			"x": text_x,
			"y": text_y,
			"x_rect": x_rect,
			"y_rect": y_rect,
			"baseline": baseline,
		}

		framedata.append(fdata)

	min_x, min_y, min_x_rect, min_y_rect = float("inf"), float("inf"), float("inf"), float("inf")
	max_x, max_y, max_x_rect, max_y_rect = 0, 0, 0, 0

	for item in framedata:
		min_x = min(min_x, item["x"])
		min_y = min(min_y, item["y"])
		max_x = max(max_x, item["x"] + item["width"])
		max_y = max(max_y, item["y"] + item["height"])
		min_x_rect = min(min_x_rect, item["x_rect"])
		min_y_rect = min(min_y_rect, item["y_rect"])
		max_x_rect = max(max_x_rect, item["x_rect"] + item["width"])
		max_y_rect = max(max_y_rect, item["y_rect"] + item["height"])

	ans = {
		"width": width,
		"height": height,
		"framedata": framedata,
		"max_width": max_width,
		"max_height": max_height,
		"max_x": max_x,
		"max_y": max_y,
		"min_x": min_x,
		"min_y": min_y,
		"max_x_rect": max_x_rect,
		"max_y_rect": max_y_rect,
		"min_x_rect": min_x_rect,
		"min_y_rect": min_y_rect,
	}

	return ans

def word_frames(frames: List[Any]) -> List[Any]:
	if not config.words:
		return frames

	worded = []
	num_words = len(config.words)

	for i, frame in enumerate(frames):
		if i >= num_words:
			worded.append(frame)
			continue

		lines = [line.strip() for line in config.words[i].split(config.linebreak)]

		if any(element.strip() for element in lines):
			frame = add_text(frame, lines)

		worded.append(frame)

	return worded

def resize_frames(frames: List[Any]) -> List[Any]:
	if config.width is None:
		return frames

	new_frames = []

	for frame in frames:
		w, h = get_shape(frame)
		ratio = w / h
		height = int(config.width / ratio)
		new_frames.append(cv2.resize(frame, (config.width, height)))

	return new_frames

def render(frames: List[Any]) -> Union[Path, None]:
	ext = utils.get_extension(config.output)
	err_msg = "Failed to make output directory"

	if ext:
		try:
			config.output.parent.mkdir(parents=False, exist_ok=True)
		except:
			utils.exit(err_msg)
			return None

		output = config.output
	else:
		try:
			config.output.mkdir(parents=False, exist_ok=True)
		except:
			utils.exit(err_msg)
			return None

		rand = utils.random_string()
		file_name = f"{rand}.{config.format}"
		output = Path(config.output, file_name)

	fmt = ext if ext else config.format

	if fmt == "gif":
		loop =  None if config.loop <= -1 else config.loop
		frames = to_pillow(frames)
		frames[0].save(output, save_all=True, append_images=frames[1:], duration=config.delay, loop=loop, optimize=True)
	elif fmt == "mp4":
		width, height = get_shape(frames[0])
		fourcc = cv2.VideoWriter_fourcc(*"mp4v")
		fps = 1000 / config.delay
		out = cv2.VideoWriter(str(output), fourcc, fps, (width, height))

		for frame in frames:
			out.write(frame)

		out.release()

	return output

def to_pillow(frames: List[Any]) -> List[Any]:
	new_frames = []

	for frame in frames:
		rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
		pil_image = Image.fromarray(rgb_frame)
		new_frames.append(pil_image)

	return new_frames

def apply_filters(frames: List[Any]) -> List[Any]:
	if (not config.filter) and (not config.filterlist):
		return frames

	new_frames = []

	min_hue = 1
	max_hue = 8
	hue_step = 20

	all_filters = [f"hue{i}" for i in range(min_hue, max_hue + 1)]
	all_filters.extend(["gray", "blur", "invert", "saturate", "none"])
	filters = []

	def get_filters() -> None:
		nonlocal filters

		if config.filteropts:
			filters = config.filteropts
		else:
			filters = all_filters

	def get_hsv(frame: Any) -> Any:
		return cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

	def do_hsv(hsv: Any) -> Any:
		return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

	def random_hue() -> str:
		return f"hue{random.randint(min_hue, max_hue)}"

	def random_filter() -> str:
		filtr = random.choice(filters)

		if not config.repeatfilter:
			filters.remove(filtr)

		if not filters:
			get_filters()

		return filtr

	get_filters()
	filtr = config.filter

	if not config.filterlist:
		if config.filter == "anyhue":
			filtr = random_hue()
		elif config.filter == "random":
			filtr = random_filter()

	for frame in frames:
		if config.filterlist:
			filtr = config.filterlist.pop(0)
		elif config.filter == "anyhue2":
			filtr = random_hue()
		elif config.filter == "random2":
			filtr = random_filter()

		new_frame = None

		for n in range(min_hue, max_hue + 1):
			if filtr == f"hue{n}":
				hsv = get_hsv(frame)
				hsv[:, :, 0] = (hsv[:, :, 0] + hue_step * n) % 180
				new_frame = do_hsv(hsv)
				break

		if new_frame is None:
			if filtr == "gray":
				new_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
				new_frame = cv2.cvtColor(new_frame, cv2.COLOR_GRAY2BGR)
			elif filtr == "blur":
				new_frame = cv2.GaussianBlur(frame, (45, 45), 0)
			elif filtr == "invert":
				new_frame = cv2.bitwise_not(frame)
			elif filtr == "saturate":
				hsv = get_hsv(frame)
				hsv[:, :, 0] = 0
				hsv[:, :, 2] = 255
				new_frame = do_hsv(hsv)
			else:
				new_frame = frame

		new_frames.append(new_frame)

	return new_frames

def get_shape(frame: Any) -> Tuple[int, int]:
	return frame.shape[1], frame.shape[0]

def count_frames() -> None:
	if config.frames is not None:
		return

	if config.framelist:
		config.frames = len(config.framelist)
	elif config.words:
		num_words = len(config.words)
		config.frames = num_words if num_words > 0 else config.frames
	else:
		config.frames = 3