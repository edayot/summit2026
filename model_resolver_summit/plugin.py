from typing import NamedTuple

from beet import Context, Font, Function, Generator, Texture
from beet.core.utils import JsonDict
from simple_item_plugin.types import NAMESPACE, Lang
from simple_item_plugin.item import Item, BlockProperties
from model_resolver.minecraft_model import DisplayOptionModel

from model_resolver.render import Render
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


    res = f"{NAMESPACE}:impl/set_screen_display/{id}"

    ctx.data.functions[res] = Function(f"""\
function ~/set_message_code:
    data modify entity @s text set value {json.dumps(message_code)}
function ~/set_message_image:
    data modify entity @s text set value {json.dumps(text_images)}
    data merge entity @s {{transformation: {{scale: [{scale}, {scale}, {scale}]}}}}
execute if entity @s[tag=model_resolver_summit.screen.code] run return run function ~/set_message_code
execute if entity @s[tag=model_resolver_summit.screen.image] run return run function ~/set_message_image
""")
    return res
    

def structure_generation_code(ctx: Context):

    font: JsonDict = {
        "providers": [{"type": "reference", "id": "minecraft:include/space"}]
    }
    font_path = f"{NAMESPACE}:font/structure"

    STRUCTURE_COOR = "186 86 -6"

    func = ctx.data.functions.setdefault(f"{NAMESPACE}:impl/loop_structure", Function("""
schedule function ~/ 100t replace
fill 186 86 -6 192 91 0 air strict
"""))
    n = 0

    char_index = 0xE000
    char_offset = 0x0005

    render = Render(ctx, default_render_size=256)
    for structure in sorted(ctx.data.structures.match("model_resolver_summit:*")):

        code = f"""\
from beet import Context

def beet_default(ctx: Context):
    render = Render(ctx)
    render.add_structure_task(
        {json.dumps(structure)}, 
        path_ctx={json.dumps(structure)}
    )
    render.run()
"""
        message_code = tokenize_code(code)

        n += 1
        char_index += char_offset

        configs = [
            (
                "iso", 
                f"\\u{char_index:04x}".encode().decode("unicode_escape"), 
                DisplayOptionModel(
                    scale=(1.5, 1.5, 1.5),
                    rotation=(30, 225, 0),
                    translation=(-16, 32, 0),
                ),
            ),
            (
                "front", 
                f"\\u{char_index+1:04x}".encode().decode("unicode_escape"), 
                DisplayOptionModel(
                    scale=(1.5, 1.5, 1.5),
                    rotation=(0, -90, 0),
                    translation=(-16, 32, 0),
                ),
            ),
            (
                "top", 
                f"\\u{char_index+2:04x}".encode().decode("unicode_escape"), 
                DisplayOptionModel(
                    scale=(1.5, 1.5, 1.5),
                    rotation=(90, 270, 0),
                    translation=(-16, 32, 0),
                ),
            ),
            (
                "left", 
                f"\\u{char_index+3:04x}".encode().decode("unicode_escape"), 
                DisplayOptionModel(
                    scale=(1.5, 1.5, 1.5),
                    rotation=(0, 0, 0),
                    translation=(-16, 32, 0),
                ),
            ),
        ]

        commands = []
        commands.append(f"data modify entity @n[tag=model_resolver_summit.structure.code, type=text_display] text set value {json.dumps(message_code)}")

        for suffix, char, display_option in configs:
            render_path = f"{NAMESPACE}:item/font/structure/{n}_{suffix}"
            render.add_structure_task(
                structure, path_ctx=render_path, animation_mode="one_file",
                display_option=display_option,
            )
            font["providers"].append(
                {
                    "type": "bitmap",
                    "file": f"{render_path}.png",
                    "ascent": 8,
                    "height": 16,
                    "chars": [char],
                }
            )
            commands.append(f"data modify entity @n[tag=model_resolver_summit.structure.{suffix}, type=text_display] text set value {json.dumps({'text': char, 'font': font_path, 'color': 'white'})}")
        

        func.append(f"""
execute 
    if score #GLOBAL_STRUCTURE model_resolver_summit.math matches {n}
    run function ~/place_structure_{n}:
        place template {structure} {STRUCTURE_COOR}
        {"\n        ".join(commands)}
""")


    func.prepend(f"""
scoreboard players add #GLOBAL_STRUCTURE model_resolver_summit.math 1
execute 
    if score #GLOBAL_STRUCTURE model_resolver_summit.math matches {n+1}.. 
    run scoreboard players set #GLOBAL_STRUCTURE model_resolver_summit.math 1
""")
    render.run()

    ctx.assets.fonts[font_path] = Font(font)

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
        # draft.cache("renders", "renders")


        renders_animated = [
            ("sculk_sensor", 4, 1),
            ("campfire", 8, 0.5),
            ("warped_hyphae", 7, 0.6),
            ("magma_block", 4, 0.75),
            ("soul_campfire", 8, 0.5),
            ("crimson_stem", 7, 0.6),
            ("command_block", 6, 0.7),
            ("sculk_shrieker", 8, 0.5),
            ("sculk", 8, 0.5),
        ]
        
        
        i = 0
        func = draft.data.functions.setdefault(f"{NAMESPACE}:impl/screen_reparts", Function("""
scoreboard players operation #SEARCH_ID model_resolver_summit.math = @s model_resolver_summit.math
"""))
        for x, y, z in renders_animated:
            res = create_animation_text(draft, x, y, z)
            func.append(f"execute if score @s model_resolver_summit.current_display matches {i} as @e[tag=model_resolver_summit.screen.part, distance=..4, predicate=model_resolver_summit:impl/search_id] run function {res}")
            i += 1
        draft.data.functions.setdefault(f"{NAMESPACE}:impl/load", Function("")).append(f"scoreboard players set #MAX model_resolver_summit.current_display {i}")


    structure_generation_code(ctx)
