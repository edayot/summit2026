from typing import NamedTuple

from beet import Context, Font, Texture
from beet.core.utils import JsonDict
from simple_item_plugin.types import NAMESPACE, Lang
from simple_item_plugin.item import Item, BlockProperties
from simple_item_plugin.crafting import ShapedRecipe, VanillaItem

from beet.contrib.messages import Message

from model_resolver.render import Render
from model_resolver.tasks.model import AnimatedResultTask
from PIL import Image
import json

from model_resolver_summit.code_style import tokenize_code


class AnimationChar(NamedTuple):
    height_small: str
    height_big: str


def create_animation_text(ctx: Context, id: str):
    path = f"minecraft:block/{id}"
    render = Render(ctx, default_render_size=256)
    task = render.add_model_task(path)
    render.run()

    font: JsonDict = {
        "providers": [{"type": "reference", "id": "minecraft:include/space"}]
    }
    font_path = f"{NAMESPACE}:font"

    char_index = 0xE000
    char_offset = 0x0004

    char_map: list[AnimationChar] = []

    for i, t in enumerate(task.tasks):
        assert isinstance(t.saved_img, Image.Image)
        char_index += char_offset

        render_path = f"{NAMESPACE}:item/font/{id}/{i}"
        ctx.assets.textures[render_path] = Texture(t.saved_img)

        char_small = f"\\u{char_index:04x}".encode().decode("unicode_escape")
        font["providers"].append(
            {
                "type": "bitmap",
                "file": f"{render_path}.png",
                "ascent": 8,
                "height": 16,
                "chars": [char_small],
            }
        )
        char_big = f"\\u{char_index+1:04x}".encode().decode("unicode_escape")
        font["providers"].append(
            {
                "type": "bitmap",
                "file": f"{render_path}.png",
                "ascent": 8,
                "height": 32,
                "chars": [char_big],
            }
        )
        char_map.append(AnimationChar(char_small, char_big))

    text: list[JsonDict | str] = [""]
    for i, (char_small, char_big) in enumerate(char_map):
        text.append(
            {
                "text": char_small + " ",
                "font": font_path,
                "color": "white",
            }
        )
        n = 4
        if i % n == n - 1:
            text.append("\n\n")

    ctx.assets.fonts[font_path] = Font(font)

    ctx.data[Message][f"{NAMESPACE}:{id}"] = Message(text)

    code = f"""\
from beet import Context

def beet_default(ctx: Context):
    render = Render(ctx)
    task = render.add_model_task(
        {json.dumps(path)}, 
        path_ctx="example:item/{id}"
    )
    render.run()
"""
    ctx.data[Message][f"{NAMESPACE}:{id}/code"] = Message(tokenize_code(code))


def beet_default(ctx: Context):
    beet_item = Item(
        id="beet", item_name=(f"{NAMESPACE}:beet", {Lang.en_us: "Beet Item"})
    ).export(ctx)

    screen = Item(
        id="screen",
        base_item="furnace",
        item_name=(f"{NAMESPACE}:screen", {Lang.en_us: "Screen"}),
        block_properties=BlockProperties(
            base_block="minecraft:barrier",
            entity_type="item_display",
        ),
    ).export(ctx)

    create_animation_text(ctx, "sculk_sensor")
