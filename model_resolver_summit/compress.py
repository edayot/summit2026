import io
from beet import Context, Texture
from PIL import Image
import numpy as np


def convert(image: Image.Image) -> Image.Image:
    if image.mode != "RGBA":
        image = image.convert("RGBA")

    arr = np.array(image)

    # Pixels totalement transparents -> RGBA (0,0,0,0)
    empty_mask = arr[:, :, 3] == 0
    arr[empty_mask] = (0, 0, 0, 0)

    image = Image.fromarray(arr, "RGBA")

    # Si peu de couleurs (cas fréquent en pixel art), on passe en mode palette (P)
    # -> 1 octet/pixel + petite palette au lieu de 4 octets/pixel en RGBA
    colors = image.getcolors(maxcolors=256)
    if colors is not None and len(colors) <= 256:
        alpha = image.getchannel("A")
        # transparence binaire uniquement (0 ou 255) -> on vérifie que c'est bien le cas
        alpha_values = set(alpha.getdata())
        if alpha_values <= {0, 255}:
            rgb = image.convert("RGB")
            quantized = rgb.convert(
                "P", palette=Image.ADAPTIVE, colors=len(colors)
            )
            # indice de transparence = premier pixel transparent trouvé
            transparent_index = None
            pal_image_data = list(zip(quantized.getdata(), alpha.getdata()))
            for idx, a in pal_image_data:
                if a == 0:
                    transparent_index = idx
                    break
            if transparent_index is not None:
                quantized.info["transparency"] = transparent_index
            image = quantized

    return image


def encode_png(image: Image.Image) -> bytes:
    buf = io.BytesIO()
    image.save(
        buf,
        format="PNG",
        optimize=True,      # active l'optimiseur de Pillow (huffman + filtres)
        compress_level=9,   # compression zlib maximale
    )
    return buf.getvalue()


def beet_default(ctx: Context):
    yield
    for path, texture in ctx.assets.textures.items():
        img = convert(texture.image)
        ctx.assets.textures[path] = Texture(encode_png(img))

    ctx.require("beet.contrib.minify_json")
    ctx.require("beet.contrib.minify_function")