from PIL import Image
from io import BytesIO
import re, base64

def base64_to_png(codec, filepath):
    img = Image.open(BytesIO(base64.b64decode(re.sub('^data:image/.+;base64,', '', codec))))
    img.save(filepath, "PNG")

def png_to_base64(filepath):
    with open(filepath, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")
