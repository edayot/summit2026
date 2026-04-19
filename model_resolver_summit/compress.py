from beet import Context, PngFile
import io
from PIL import Image

def to_bytes(self, content: Image.Image) -> bytes:
    dst = io.BytesIO()
    content.save(dst, format="png", optimize=True, compress_level=9)
    return dst.getvalue()


def beet_default(ctx: Context):
    PngFile.to_bytes = to_bytes
    yield
    ctx.require("beet.contrib.minify_json")
    ctx.require("beet.contrib.minify_function")



