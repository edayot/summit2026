from pathlib import Path
from typing import NamedTuple

from beet import Context, Draft, Font, Function, ResourcePack, Texture, Generator
from beet.core.utils import JsonDict
from simple_item_plugin.types import NAMESPACE, Lang
from simple_item_plugin.item import Item, BlockProperties
from model_resolver.minecraft_model import DisplayOptionModel
from model_resolver.pack_getter import PackGetterLookup
from model_resolver.item_model.item import Item as ModelResolverItem

from model_resolver.render import Render, StructureRenderTask # pyright: ignore[reportPrivateImportUsage]
from PIL import Image
import json
import os

from model_resolver_summit.code_style import tokenize_code


class AnimationChar(NamedTuple):
    height_small: str
    height_big: str


def create_animation_text(draft: Generator, id: str, n: int = 4, scale: float = 1):
    path = f"minecraft:block/{id}"
    render = Render(draft.ctx, default_render_size=64)
    task = render.add_model_task(path)
    render.run()

    font: JsonDict = {
        "providers": [{"type": "reference", "id": "minecraft:include/space"}]
    }
    font_path = f"{NAMESPACE}:{id}"

    char_index = 0xE000
    char_offset = 0x0004

    char_map: list[AnimationChar] = []

    images = [t.saved_img for t in task.tasks]
    for img in images:
        assert isinstance(img, Image.Image)

    # taille de cellule = taille d'un rendu (identiques car default_render_size fixe)
    cell_w, cell_h = images[0].size
    cols = n
    rows = -(-len(images) // cols)  # ceil division

    # une seule image regroupant tous les rendus
    sheet = Image.new("RGBA", (cell_w * cols, cell_h * rows), (0, 0, 0, 0))

    small_rows: list[str] = []
    big_rows: list[str] = []

    for r in range(rows):
        small_row = ""
        big_row = ""
        for c in range(cols):
            i = r * cols + c
            char_index += char_offset
            char_small = f"\\u{char_index:04x}".encode().decode("unicode_escape")
            char_big = f"\\u{char_index + 1:04x}".encode().decode("unicode_escape")

            if i < len(images):
                sheet.paste(images[i], (c * cell_w, r * cell_h))
                char_map.append(AnimationChar(char_small, char_big))
            # sinon : cellule vide (padding), le char n'est jamais utilisé dans text_images

            small_row += char_small
            big_row += char_big

        small_rows.append(small_row)
        big_rows.append(big_row)

    render_path = f"{NAMESPACE}:item/font/{id}"
    draft.assets.textures[render_path] = Texture(sheet)

    font["providers"].append(
        {
            "type": "bitmap",
            "file": f"{render_path}.png",
            "ascent": 8,
            "height": 16,
            "chars": small_rows,
        }
    )
    font["providers"].append(
        {
            "type": "bitmap",
            "file": f"{render_path}.png",
            "ascent": 8,
            "height": 32,
            "chars": big_rows,
        }
    )

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

    draft.assets.fonts[font_path] = Font(font)

    code = f"""\
from beet import Context
from model_resolver import Render
                                                                          
def beet_default(ctx: Context):
    render = Render(ctx)
    task = render.add_model_task(
        {json.dumps(path)}, 
        path_ctx="example:item/{id}"
    )
    render.run()
"""
    message_code = tokenize_code(code)

    res = f"{NAMESPACE}:v0.1.0/set_screen_display/{id}"

    draft.data.functions[res] = Function(f"""\
function ~/set_message_code:
    data modify entity @s text set value {json.dumps(message_code)}
function ~/set_message_image:
    data modify entity @s text set value {json.dumps(text_images)}
    data merge entity @s {{transformation: {{scale: [{scale}, {scale}, {scale}]}}}}
execute if entity @s[tag=model_resolver_summit.screen.code] run return run function ~/set_message_code
execute if entity @s[tag=model_resolver_summit.screen.image] run return run function ~/set_message_image
""")
    lore_lines: list[JsonDict | str] = [""]
    for i, (char_small, char_big) in enumerate(char_map):
        lore_lines.append(
            {
                "text": char_small + " ",
                "font": font_path,
                "color": "white",
            }
        )
        if i % n == n - 1:
            lore_lines.append("\n\n")

    tellraw_message = [
        "",
        {"text": "[Model Resolver Summit] ", "color": "green"},
        {"text": "Switching to "},
        {
            "text": char_map[0][0] + "\n",
            "font": font_path,
            "hover_event": {
                "action": "show_text",
                "value": lore_lines,
            },
        },
    ]

    message_res = f"{NAMESPACE}:v0.1.0/switch_message/{id}"
    draft.data.functions[message_res] = Function(
        f"tellraw @s {json.dumps(tellraw_message)}"
    )

    return res, message_res
    

def structure_generation_code(draft: Generator):

    font: JsonDict = {
        "providers": [{"type": "reference", "id": "minecraft:include/space"}]
    }
    font_path = f"{NAMESPACE}:font/structure"

    STRUCTURE_COOR = "186 86 -6"

    func = draft.data.functions.setdefault(f"{NAMESPACE}:v0.1.0/loop_structure", Function("""
schedule function ~/ 100t replace
fill 186 86 -6 192 91 0 air strict
"""))
    n = 0

    char_index = 0xE000
    char_offset = 0x0005

    # au lieu de {render_path: task}, on garde la structure groupée par n
    # pour pouvoir reconstituer la grille 2x2 après le render.run()
    tasks_by_structure: dict[int, dict[str, StructureRenderTask]] = {}

    render = Render(draft.ctx, default_render_size=256)
    render.getter._custom = PackGetterLookup(assets=ResourcePack(path=Path(__file__).parent.parent / "private" / "summit-rp.zip"))  # pyright: ignore[reportAttributeAccessIssue]
    render.getter.lookups.insert(0, "_custom")
    render.getter._simpledrawer = PackGetterLookup(assets=ResourcePack(path=Path(__file__).parent.parent / "private" / "simpledrawer-rp.zip"))  # pyright: ignore[reportAttributeAccessIssue]
    render.getter.lookups.insert(0, "_simpledrawer")

    for structure in sorted(draft.ctx.data.structures.match("model_resolver_summit:*")):

        code = f"""\
from beet import Context
from model_resolver import Render

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
                f"\\u{char_index + 1:04x}".encode().decode("unicode_escape"),
                DisplayOptionModel(
                    scale=(1.5, 1.5, 1.5),
                    rotation=(0, -90, 0),
                    translation=(-16, 32, 0),
                ),
            ),
            (
                "top",
                f"\\u{char_index + 2:04x}".encode().decode("unicode_escape"),
                DisplayOptionModel(
                    scale=(1.5, 1.5, 1.5),
                    rotation=(90, 270, 0),
                    translation=(-16, 32, 0),
                ),
            ),
            (
                "left",
                f"\\u{char_index + 3:04x}".encode().decode("unicode_escape"),
                DisplayOptionModel(
                    scale=(1.5, 1.5, 1.5),
                    rotation=(0, 0, 0),
                    translation=(-16, 32, 0),
                ),
            ),
        ]

        commands = []
        commands.append(f"data modify entity @e[tag=model_resolver_summit.structure.code, type=text_display, distance=..10, limit=1] text set value {json.dumps(message_code)}")

        # un seul fichier texture pour les 4 vues de cette structure
        render_path = f"{NAMESPACE}:item/font/structure/{n}"
        structure_tasks: dict[str, StructureRenderTask] = {}

        for suffix, char, display_option in configs:
            structure_tasks[suffix] = render.add_structure_task(
                structure, animation_mode="one_file",
                display_option=display_option,
            )
            commands.append(
                f"data modify entity @e[tag=model_resolver_summit.structure.{suffix}, type=text_display, distance=..10, limit=1] text set value "
                f"{json.dumps({'text': char, 'font': font_path, 'color': 'white'})}"
            )

        tasks_by_structure[n] = structure_tasks

        # grille 2x2 : ligne 0 = iso, front / ligne 1 = top, left
        grid_chars = [
            configs[0][1] + configs[1][1],
            configs[2][1] + configs[3][1],
        ]

        font["providers"].append(
            {
                "type": "bitmap",
                "file": f"{render_path}.png",
                "ascent": 8,
                "height": 16,
                "chars": grid_chars,
            }
        )

        func.append(f"""
execute 
    if score #GLOBAL_STRUCTURE model_resolver_summit.math matches {n}
    positioned 203 88 -3
    run return run function ~/place_structure_{n}:
        place template {structure} {STRUCTURE_COOR} none none 1 0 strict
        {"\n        ".join(commands)}
""")

    func.prepend(f"""
scoreboard players add #GLOBAL_STRUCTURE model_resolver_summit.math 1
execute 
    if score #GLOBAL_STRUCTURE model_resolver_summit.math matches {n+1}.. 
    run scoreboard players set #GLOBAL_STRUCTURE model_resolver_summit.math 1
""")
    render.run()

    def resolve_image(task: StructureRenderTask) -> Image.Image:
        if task.tasks:
            img = task.tasks[0].saved_img
        else:
            img = task.saved_img
        assert isinstance(img, Image.Image)
        return img

    for n, structure_tasks in tasks_by_structure.items():
        images = {
            suffix: resolve_image(task)
            for suffix, task in structure_tasks.items()
        }

        # taille de cellule commune = max sur les 4 vues, pour un découpage
        # en grille régulier côté client (division égale de l'image)
        cell_w = max(img.width for img in images.values())
        cell_h = max(img.height for img in images.values())

        sheet = Image.new("RGBA", (cell_w * 2, cell_h * 2), (0, 0, 0, 0))
        positions = {
            "iso": (0, 0),
            "front": (1, 0),
            "top": (0, 1),
            "left": (1, 1),
        }
        for suffix, img in images.items():
            col, row = positions[suffix]
            # on centre l'image dans la cellule si elle est plus petite que cell_w/h
            offset_x = col * cell_w + (cell_w - img.width) // 2
            offset_y = row * cell_h + (cell_h - img.height) // 2
            sheet.paste(img, (offset_x, offset_y))

        render_path = f"{NAMESPACE}:item/font/structure/{n}"
        draft.assets.textures[render_path] = Texture(sheet)

    draft.assets.fonts[font_path] = Font(font)

def render_banner(draft: Draft):
    render = Render(draft.ctx)
    task = render.add_item_task(
        ModelResolverItem(
            id="minecraft:white_banner",
            components={
                "minecraft:item_name": {"translate": "block.minecraft.ominous_banner"}, 
                "minecraft:tooltip_display": {"hidden_components": ["minecraft:banner_patterns"]}, 
                "minecraft:rarity": "uncommon", 
                "minecraft:banner_patterns": [
                    {"color": "cyan",           "pattern": "minecraft:rhombus"}, 
                    {"color": "light_gray",     "pattern": "minecraft:stripe_bottom"}, 
                    {"color": "gray",           "pattern": "minecraft:stripe_center"}, 
                    {"color": "light_gray",     "pattern": "minecraft:border"}, 
                    {"color": "black",          "pattern": "minecraft:stripe_middle"}, 
                    {"color": "light_gray",     "pattern": "minecraft:half_horizontal"}, 
                    {"color": "light_gray",     "pattern": "minecraft:circle"}, 
                    {"color": "black",          "pattern": "minecraft:border"}
                ]
            }
        ),
        render_size=256,
    )
    render.run()
    render_path = f"{NAMESPACE}:item/ominous_banner"
    draft.assets.textures[render_path] = Texture(task.saved_img)

    font: JsonDict = {
        "providers": [{"type": "reference", "id": "minecraft:include/space"}]
    }
    char = f"\\u{0xE000:04x}".encode().decode("unicode_escape")
    font["providers"].append(
        {
            "type": "bitmap",
            "file": f"{render_path}.png",
            "ascent": 24,
            "height": 48,
            "chars": [char],
        }
    )
    font_path = f"{NAMESPACE}:ominous_banner"
    draft.assets.fonts[font_path] = Font(font)
    draft.data.functions[f"{NAMESPACE}:v0.1.0/display_in_chat/ominous_banner"] = Function(
        f"tellraw @s {json.dumps(["", {'text': f"\n\n{char}", 'font': font_path, 'color': 'white'},"        This is a render of an Ominous Banner !\n\n\n"])}"
    )


def beet_default(ctx: Context):
    # screen = Item(
    #     id="screen",
    #     base_item="furnace",
    #     item_name=(f"{NAMESPACE}:screen", {Lang.en_us: "Screen"}),
    #     block_properties=BlockProperties(
    #         base_block="minecraft:air",
    #         entity_type="item_display",
    #         destroy_code=False
    #     ),
    # ).export(ctx)

    code = """\
from beet import Context
from model_resolver import Render, Item

def beet_default(ctx: Context):
    render = Render(ctx)
    item = Item(
        id="minecraft:white_banner",
        components={
            "minecraft:item_name": {"translate": "block.minecraft.ominous_banner"}, 
            "minecraft:banner_patterns": [
                {"color": "cyan",           "pattern": "minecraft:rhombus"}, 
                {"color": "light_gray",     "pattern": "minecraft:stripe_bottom"}, 
                {"color": "gray",           "pattern": "minecraft:stripe_center"}, 
                {"color": "light_gray",     "pattern": "minecraft:border"}, 
                {"color": "black",          "pattern": "minecraft:stripe_middle"}, 
                {"color": "light_gray",     "pattern": "minecraft:half_horizontal"}, 
                {"color": "light_gray",     "pattern": "minecraft:circle"}, 
                {"color": "black",          "pattern": "minecraft:border"}
            ]
        }
    )
    render.add_item_task(item, path_ctx="minecraft:ominous_banner")
    render.run()

"""
    message_code = tokenize_code(code, lexer="python")
    command = f"data modify entity @n[type=text_display] text set value {json.dumps(message_code)}"

    # func = ctx.data.functions.setdefault(f"{NAMESPACE}:v0.1.0/set_text_ominous_banner", Function(command))


    with ctx.generate.draft() as draft:
        draft.cache("banner", "banner")
        render_banner(draft)

    with ctx.generate.draft() as draft:
        key = ""
        for struct in sorted(ctx.data.structures.match("model_resolver_summit:*")):
            s = ctx.data.structures[struct]
            time = None
            if s.source_path:
                time = os.path.getmtime(s.source_path)
            key = key + f"{struct} {time}\n"
        draft.cache("structure", key)
        structure_generation_code(draft)
    renders_animated = [
        ("sculk_sensor", 4, 1),
        ("calibrated_sculk_sensor", 4, 1),
        ("sculk_shrieker", 8, 0.5),
        ("sculk", 8, 0.5),
        ("campfire", 8, 0.5),
        ("soul_campfire", 8, 0.5),
        ("warped_hyphae", 7, 0.6),
        ("crimson_stem", 7, 0.6),
        ("magma_block", 4, 0.75),
        ("respawn_anchor_2", 6, 0.7),
        ("command_block", 6, 0.7),
        ("chain_command_block", 6, 0.7),
        ("repeating_command_block", 6, 0.7),
        ("seagrass", 4, 0.75),
        ("kelp", 4, 0.75),
    ]
    with ctx.generate.draft() as draft:
        draft.cache("renders", str(renders_animated))
        i = 0
        func = draft.data.functions.setdefault(f"{NAMESPACE}:v0.1.0/screen_reparts", Function(""))
        for x, y, z in renders_animated:
            res, message_res = create_animation_text(draft, x, y, z)
            func.append(f"""
execute 
    if score @s model_resolver_summit.current_display matches {i}  
    run return run function ~/change_to_{i}:
        execute as @e[type=#model_resolver_summit:screen_part, tag=model_resolver_summit.screen.part, distance=..16] run function {res}
        execute on target run function {message_res}
        execute on attacker run function {message_res}
    """)
            i += 1
        draft.data.functions.setdefault(f"{NAMESPACE}:v0.1.0/load_set_max").append(f"scoreboard players set #MAX model_resolver_summit.current_display {i}")


