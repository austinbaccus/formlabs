import base64
import requests
from io import BytesIO
from PIL import Image
from pathlib import Path

def _to_bilevel(img: Image.Image, threshold: int = 128) -> Image.Image:
    return (img.convert("L")
               .point(lambda p: 255 if p >= threshold else 0) # type: ignore
               .convert("1", dither=Image.Dither.NONE)) # converting from 8-bit depth to 1-bit depth... the original images are black and white, so only 1-bit depth is needed

# I'm going to leave `fetch_image_web` here - I used this to download the images for testing, although it is not used anymore.
# I am not sure if the "spirit" of this test is to handle downloading images from a server or if downloading them from a URL is simply an easy way for candidates to access the images.
# I'm choosing to download them once to make testing and validation easier for me and whoever tests my code. It's much faster.
# However, in case network retrieval is an important part of the test, I'm leaving this in so that one could easily switch `image_data = fetch_image_local("images", file_name)` to `image_data = fetch_image_web(image_url)` in the `print_layer.from_csv_row()` function.
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

def image_to_file(image: Image.Image, path: str, filename: str) -> str:
    dest = Path(path)
    dest.mkdir(parents=True, exist_ok=True)
    full_path = dest / filename
    image.save(full_path, format="TIFF", compression="group4") # converting to TIFF instead of PNG. I was able to get the image file from 5KB to ~1-2KB this way (along with the reduction from 8-bit depth to 1-bit depth)
    return str(full_path)