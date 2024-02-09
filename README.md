<img src="borat.jpg" width="350">

This is a python program to produce gif images.

It extracts random frames from a video.

It (optionally) places words somewhere on each frame.

Then joins all frames into an animated gif.

## Why?

It might be useful in the realm of human verification.

And memes.

## Installation

Clone this repo, and get inside the dir.

```
git clone --depth=1 https://github.com/madprops/borat

cd borat
```

Then create the virtual env:

```
python -m venv venv
```

Then install the dependencies:

```
venv/bin/pip install -r requirements.txt
```

## Usage

You can provide any video path using the `--video` flag:

```
venv/bin/python borat.py --video="/path/to/video.webm"
```

`webm` and `mp4` should work, and maybe other formats.

You can pass it a string of lines to use on each frame.

They are separated by ";" (semicolons).

```
venv/bin/python borat.py --words="Hello Brother; Construct Additional Pylons"
```

It will make 2 frames, one per line.

If you want to make a gif with 5 random frames and an FPS of 3:

```
venv/bin/python borat.py --frames=5 --fps=3
```

You can use random words with `[random]`:

```
venv/bin/python borat.py --words="I Like [random] and [random]"
```

It will pick random words from a list of english words.

There are 3 kinds of random formats: `[random]`, `[RANDOM]`, and `[Random]`.

The replaced word will use the casing of those.

For example `[RANDOM]` might be `PLANET`.

## Defaults

It uses these defaults (defined in `borat.py`):

```
FPS = 2.2
FRAMES = 3
SIZE = 3
THICK = 3
LEFT = None
TOP = None
```

`FPS` (frames per second) modifies the speed between frame change (ms).

A bigger `FPS` = A faster gif.

`FRAMES` is the amount of frames to use if `--words` is not used.

`LEFT` is the padding from the left edge.

`TOP` is the padding from the top edge.

If these are not set then the text is placed in the center.

`SIZE` and `THICK` modify the text's size and thickness.

All of these can be changed with flags like `--fps=3 --top=0`

---

<img src="borat.gif" width="600">