from typing import NamedTuple

from beet import Context, Font, Function, Generator, Texture
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


def create_animation_text(ctx: Generator, id: str, n=4, scale: float = 1):
    path = f"minecraft:block/{id}"
    render = Render(ctx.ctx, default_render_size=256)
    task = render.add_model_task(path)
    render.run()

    font: JsonDict = {
        "providers": [{"type": "reference", "id": "minecraft:include/space"}]
    }
    font_path = f"{NAMESPACE}:font/{id}"

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

    text_images: list[JsonDict | str] = [""]
    for i, (char_small, char_big) in enumerate(char_map):
        text_images.append(
            {
                "text": char_small + " ",
                "font": font_path,
                "color": "white",
            }
        )
        if i % n == n - 1:
            text_images.append("\n\n")

    ctx.assets.fonts[font_path] = Font(font)

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
    message_code = tokenize_code(code)


    ctx.data.functions[f"{NAMESPACE}:impl/set_screen_display/{id}"] = Function(f"""\
function ~/set_message_code:
    data modify entity @s text set value {json.dumps(message_code)}
function ~/set_message_image:
    data modify entity @s text set value {json.dumps(text_images)}
    data merge entity @s {{transformation: {{scale: [{scale}, {scale}, {scale}]}}}}
execute if entity @s[tag=model_resolver_summit.screen.code] run return run function ~/set_message_code
execute if entity @s[tag=model_resolver_summit.screen.image] run return run function ~/set_message_image
execute as @n[tag=model_resolver_summit.screen.code, distance=..10] run function ~/set_message_code
execute as @n[tag=model_resolver_summit.screen.image, distance=..10] run function ~/set_message_image
""")


def beet_default(ctx: Context):
    screen = Item(
        id="screen",
        base_item="furnace",
        item_name=(f"{NAMESPACE}:screen", {Lang.en_us: "Screen"}),
        block_properties=BlockProperties(
            base_block="minecraft:air",
            entity_type="item_display",
            destroy_code=False
        ),
    ).export(ctx)

    with ctx.generate.draft() as draft:
        draft.cache("guide", "guide")
        create_animation_text(draft, "sculk_sensor")
        create_animation_text(draft, "campfire", 8, 0.5)
        create_animation_text(draft, "warped_hyphae", 6, 0.75)
