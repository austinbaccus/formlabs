import base64
import requests
from io import BytesIO
from PIL import Image
from pathlib import Path

def _to_bilevel(img: Image.Image, threshold: int = 128) -> Image.Image:
    return (img.convert("L")
               .point(lambda p: 255 if p >= threshold else 0) # type: ignore
               .convert("1", dither=Image.Dither.NONE)) # converting from 8-bit depth to 1-bit depth... the original images are black and white, so only 1-bit depth is needed

def fetch_image_web(url: str) -> Image.Image | None:
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        img = Image.open(BytesIO(resp.content))
        return _to_bilevel(img)
    except (requests.RequestException, OSError):
        return None

def fetch_image_local(path: str, filename: str) -> Image.Image | None:
    try:
        img = Image.open(Path(path) / filename)
        return _to_bilevel(img)
    except OSError:
        return None

def image_to_string(image: Image.Image) -> str:
    buf = BytesIO()
    image.save(buf, format="TIFF", compression="group4")
    return base64.b64encode(buf.getvalue()).decode("ascii")