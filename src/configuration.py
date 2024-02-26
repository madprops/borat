# Modules
import utils
from argparser import ArgParser

# Standard
import codecs
import textwrap
import random
from argparse import Namespace
from typing import List, Union, Dict, Tuple, Any
from PIL import ImageFont  # type: ignore
from pathlib import Path


class Configuration:
    # Class to hold all the configuration of the program
    # It also interfaces with ArgParser and processes further

    delay = 700
    frames: Union[int, None] = None
    left: Union[int, None] = None
    right: Union[int, None] = None
    top: Union[int, None] = None
    bottom: Union[int, None] = None
    width: Union[int, None] = None
    height: Union[int, None] = None
    words: List[str] = []
    wordfile: Union[Path, None] = None
    randomlist: List[str] = []
    separator = ";"
    format = "gif"
    order = "random"
    font = "sans"
    fontsize = 60
    fontcolor: Union[Tuple[int, int, int], str] = (255, 255, 255)
    bgcolor: Union[Tuple[int, int, int], str, None] = None
    outline: Union[Tuple[int, int, int], str, None] = None
    outlinewidth = 2
    noleftoutline = False
    norightoutline = False
    notopoutline = False
    nobottomoutline = False
    opacity = 0.66
    padding = 20
    radius = 0
    align = "center"
    script: Union[Path, None] = None
    loop = 0
    remake = False
    filterlist: List[str] = []
    filteropts: List[str] = []
    filter = "none"
    framelist: List[str] = []
    frameopts: List[str] = []
    repeatrandom = False
    repeatfilter = False
    fillwords = False
    fillgen = False
    nogrow = False
    wrap = 35
    nowrap = False
    verbose = False
    descender = False
    seed: Union[int, None] = None
    frameseed: Union[int, None] = None
    wordseed: Union[int, None] = None
    filterseed: Union[int, None] = None
    deepfry = False
    vertical = False
    horizontal = False

    # --- INTERAL VARS

    # List to keep track of used random words
    randwords: List[str] = []

    # Counter for [count]
    wordcount = 0

    # Last font color used
    last_fontcolor: Union[Tuple[int, int, int], None] = None

    # Random generators
    random_frames: Union[random.Random, None] = None
    random_words: Union[random.Random, None] = None
    random_filters: Union[random.Random, None] = None

    def get_argdefs(self) -> Tuple[List[Dict[str, Any]], Dict[str, List[str]]]:
        rgbstr = "3 numbers from 0 to 255, separated by commas. Names like 'yellow' are also supported"
        commastr = "Separated by commas"

        argdefs: List[Dict[str, Any]] = [
            {"name": "input", "type": str,
             "help": "Path to the a video or image file. Separated by commas"},

            {"name": "words", "type": str,
             "help": "Lines of words to use on the frames"},

            {"name": "wordfile", "type": str,
             "help": "Path of file with word lines"},

            {"name": "delay", "type": str,
             "help": "The delay in ms between frames"},

            {"name": "left", "type": int,
             "help": "Left padding"},

            {"name": "right", "type": int,
             "help": "Right padding"},

            {"name": "top", "type": int,
             "help": "Top padding"},

            {"name": "bottom", "type": int,
             "help": "Bottom padding"},

            {"name": "width", "type": int,
             "help": "Width to resize the frames"},

            {"name": "height", "type": int,
             "help": "Height to resize the frames"},

            {"name": "frames", "type": int,
             "help": "Number of frames to use if no words are provided"},

            {"name": "output", "type": str,
             "help": "Output directory to save the file"},

            {"name": "format", "type": str,
             "choices": ["gif", "webm", "mp4", "jpg", "png"],
             "help": "The format of the output file"},

            {"name": "separator", "type": str,
             "help": "Character to use as the separator"},

            {"name": "order", "type": str,
             "choices": ["random", "normal"],
             "help": "The order to use when extracting the frames"},

            {"name": "font", "type": str,
             "help": "The font to use for the text"},

            {"name": "fontsize", "type": str,
             "help": "The size of the font"},

            {"name": "fontcolor", "type": str,
             "help": f"Text color. {rgbstr}"},

            {"name": "bgcolor", "type": str,
             "help": f"Add a background rectangle for the text with this color. {rgbstr}"},

            {"name": "outline", "type": str,
             "help": f"Add an outline around the text with this color. {rgbstr}"},

            {"name": "outlinewidth", "type": str,
             "help": "The width of the outline"},

            {"name": "opacity", "type": str,
             "help": "The opacity of the background rectangle"},

            {"name": "padding", "type": str,
             "help": "The padding of the background rectangle"},

            {"name": "radius", "type": str,
             "help": "The border radius of the background"},

            {"name": "align", "type": str,
             "choices": ["left", "center", "right"],
             "help": "How to align the center when there are multiple lines"},

            {"name": "randomlist", "type": str,
             "help": "List of words to consider for random words"},

            {"name": "randomfile", "type": str,
             "help": "Path to a list of words to consider for random words"},

            {"name": "script", "type": str,
             "help": "Path to a TOML file that defines the arguments to use"},

            {"name": "loop", "type": int,
             "help": "How to loop a gif render"},

            {"name": "remake", "action": "store_true",
             "help": "Re-render the frames to change the width or delay"},

            {"name": "filter", "type": str,
             "choices": ["hue1", "hue2", "hue3", "hue4", "hue5", "hue6", "hue7", "hue8", "anyhue", "anyhue2",
                         "gray", "blur", "invert", "random", "random2", "none"],
             "help": "Color filter to apply to frames"},

            {"name": "filterlist", "type": str,
             "help": f"Filters to use per frame. {commastr}"},

            {"name": "filteropts", "type": str,
             "help": f"The list of allowed filters when picking randomly. {commastr}"},

            {"name": "framelist", "type": str,
             "help": f"List of frame indices to use. {commastr}"},

            {"name": "frameopts", "type": str,
             "help": f"The list of allowed frame indices when picking randomly. {commastr}"},

            {"name": "repeatrandom", "action": "store_true",
             "help": "Repeating random words is ok"},

            {"name": "repeatfilter", "action": "store_true",
             "help": "Repeating random filters is ok"},

            {"name": "fillwords", "action": "store_true",
             "help": "Fill the rest of the frames with the last word line"},

            {"name": "fillgen", "action": "store_true",
             "help": "Generate the first line of words till the end of frames"},

            {"name": "nogrow", "action": "store_true",
             "help": "Don't resize if the frames are going to be bigger than the original"},

            {"name": "wrap", "type": str,
             "help": "Split line if it exceeds this char length"},

            {"name": "nowrap", "action": "store_true",
             "help": "Don't wrap lines"},

            {"name": "noleftoutline", "action": "store_true",
             "help": "Don't draw the left outline"},

            {"name": "norightoutline", "action": "store_true",
             "help": "Don't draw the right outline"},

            {"name": "notopoutline", "action": "store_true",
             "help": "Don't draw the top outline"},

            {"name": "nobottomoutline", "action": "store_true",
             "help": "Don't draw the bottom outline"},

            {"name": "verbose", "action": "store_true",
             "help": "Print more information like time performance"},

            {"name": "descender", "action": "store_true",
             "help": "Apply the height of the descender to the bottom padding of the text"},

            {"name": "seed", "type": int,
             "help": "Seed to use when using any random value"},

            {"name": "frameseed", "type": int,
             "help": "Seed to use when picking frames"},

            {"name": "wordseed", "type": int,
             "help": "Seed to use when picking words"},

            {"name": "filterseed", "type": int,
             "help": "Seed to use when picking filters"},

            {"name": "deepfry", "action": "store_true",
             "help": "Compress the frames heavily"},

            {"name": "vertical", "action": "store_true",
             "help": "Append images vertically"},

            {"name": "horizontal", "action": "store_true",
             "help": "Append images horizontally"},
        ]

        aliases = {
            "input": ["--i", "-i"],
            "output": ["--o", "-o"],
        }

        return argdefs, aliases

    def parse_args(self) -> None:
        argdefs, aliases = self.get_argdefs()
        ap = ArgParser("Gif Maker", argdefs, aliases, self)

        # ---

        ap.path("script")
        self.check_script(ap.args)

        # ---

        string_arg = ap.string_arg()

        if string_arg:
            ap.args.words = string_arg

        # ---

        ap.number("fontsize", int)
        ap.number("delay", int, duration=True)
        ap.number("opacity", float, allow_zero=True)
        ap.number("padding", int, allow_zero=True)
        ap.number("radius", int, allow_zero=True)
        ap.number("outlinewidth", int)
        ap.number("wrap", int)

        # ---

        ap.commas("framelist", int)
        ap.commas("frameopts", int)
        ap.commas("filterlist", str)
        ap.commas("filteropts", str)
        ap.commas("fontcolor", int, allow_string=True, is_tuple=True)
        ap.commas("bgcolor", int, allow_string=True, is_tuple=True)
        ap.commas("outline", int, allow_string=True, is_tuple=True)

        # ---

        normals = ["left", "right", "top", "bottom", "width", "height", "format", "order",
                   "font", "frames", "loop", "separator", "filter", "remake", "repeatrandom",
                   "repeatfilter", "fillwords", "nogrow", "align", "nowrap", "noleftoutline",
                   "norightoutline", "notopoutline", "nobottomoutline", "verbose", "fillgen",
                   "descender", "seed", "frameseed", "wordseed", "filterseed", "deepfry",
                   "vertical", "horizontal"]

        for normal in normals:
            ap.normal(normal)

        # ---

        paths = ["output", "wordfile", "randomfile"]

        for path in paths:
            ap.path(path)

        # ---

        pathlists = ["input"]

        for pathlist in pathlists:
            ap.pathlist(pathlist)

        # ---

        self.check_config(ap.args)

    def check_config(self, args: Namespace) -> None:
        def separate(value: str) -> List[str]:
            return [codecs.decode(utils.clean_lines(item), "unicode-escape")
                    for item in value.split(self.separator)]

        for path in self.input:
            if not path.exists() or not path.is_file():
                utils.exit("Input file does not exist")
                return

        if self.wordfile:
            if not self.wordfile.exists() or not self.wordfile.is_file():
                utils.exit("Word file does not exist")
                return

            self.read_wordfile()
        elif args.words:
            self.words = separate(args.words)

        if args.randomlist:
            self.randomlist = separate(args.randomlist)

        if not self.randomfile.exists() or not self.randomfile.is_file():
            utils.exit("Word file does not exist")
            return

        if not self.nowrap:
            self.wrap_text("words")

        self.set_random()

    def wrap_text(self, attr: str) -> None:
        lines = getattr(self, attr)

        if not lines:
            return

        new_lines = []

        for line in lines:
            lines = line.split("\n")
            wrapped = [textwrap.fill(x, self.wrap) for x in lines]
            new_lines.append("\n".join(wrapped))

        setattr(self, attr, new_lines)

    def check_script(self, args: Namespace) -> None:
        if self.script is None:
            return

        data = utils.read_toml(Path(self.script))

        if data:
            for key in data:
                k = key.replace("-", "_")
                setattr(args, k, data[key])

    def read_wordfile(self) -> None:
        if self.wordfile:
            self.words = self.wordfile.read_text().splitlines()

    def fill_paths(self, main_file: str) -> None:
        self.root = utils.full_path(Path(main_file).parent.parent)
        self.input = [utils.full_path(Path(self.root, "media", "video.webm"))]
        self.output = utils.full_path(Path(self.root, "output"))
        self.randomfile = utils.full_path(Path(self.root, "data", "nouns.txt"))
        self.fontspath = utils.full_path(Path(self.root, "fonts"))

    def get_color(self, attr: str) -> Tuple[int, int, int]:
        value = getattr(self, attr)
        rgb: Union[Tuple[int, int, int], None] = None
        set_config = False

        if isinstance(value, str):
            if value == "light":
                rgb = utils.random_light()
                set_config = True
            elif value == "light2":
                rgb = utils.random_light()
            elif value == "dark":
                rgb = utils.random_dark()
                set_config = True
            elif value == "dark2":
                rgb = utils.random_dark()
            elif (value == "font") and isinstance(self.last_fontcolor, tuple):
                rgb = self.last_fontcolor
            elif value == "lightfont" and isinstance(self.last_fontcolor, tuple):
                rgb = utils.light_contrast(self.last_fontcolor)
                set_config = True
            elif value == "lightfont2" and isinstance(self.last_fontcolor, tuple):
                rgb = utils.light_contrast(self.last_fontcolor)
            elif value == "darkfont" and isinstance(self.last_fontcolor, tuple):
                rgb = utils.dark_contrast(self.last_fontcolor)
                set_config = True
            elif value == "darkfont2" and isinstance(self.last_fontcolor, tuple):
                rgb = utils.dark_contrast(self.last_fontcolor)
            else:
                rgb = utils.color_name(value)
        elif isinstance(value, (list, tuple)) and len(value) >= 3:
            rgb = (value[0], value[1], value[2])

        ans = rgb or (100, 100, 100)

        if attr == "fontcolor":
            config.last_fontcolor = ans

        if set_config:
            setattr(self, attr, rgb)

        return ans

    def set_random(self) -> None:
        def set_rng(attr: str, rng_name: str) -> None:
            value = getattr(self, attr)

            if value is not None:
                rand = random.Random(value)
            elif self.seed is not None:
                rand = random.Random(self.seed)
            else:
                rand = random.Random()

            setattr(self, rng_name, rand)

        set_rng("frameseed", "random_frames")
        set_rng("wordseed", "random_words")
        set_rng("filterseed", "random_filters")

    def get_font(self) -> ImageFont.FreeTypeFont:
        fonts = {
            "sans": "Roboto-Regular.ttf",
            "serif": "RobotoSerif-Regular.ttf",
            "mono": "RobotoMono-Regular.ttf",
            "italic": "Roboto-Italic.ttf",
            "bold": "Roboto-Bold.ttf",
            "cursive": "Pacifico-Regular.ttf",
            "comic": "ComicNeue-Regular.ttf",
            "nova": "NovaSquare-Regular.ttf",
        }

        def random_font() -> str:
            return random.choice(list(fonts.keys()))

        if config.font == "random":
            font = random_font()
            font_file = fonts[font]
            config.font = font
        elif config.font == "random2":
            font = random_font()
            font_file = fonts[font]
        elif ".ttf" in config.font:
            font_file = str(utils.resolve_path(Path(config.font)))
        elif config.font in fonts:
            font_file = fonts[config.font]
        else:
            font_file = fonts["sans"]

        path = Path(config.fontspath, font_file)
        return ImageFont.truetype(path, size=config.fontsize)


# Main configuration object
config = Configuration()
