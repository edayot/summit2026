from beet import Context, Font, Texture
from beet.core.utils import JsonDict
from simple_item_plugin.types import NAMESPACE, Lang
from simple_item_plugin.item import Item, BlockProperties
from simple_item_plugin.crafting import ShapedRecipe, VanillaItem

from beet.contrib.messages import Message

from model_resolver.render import Render
from model_resolver.tasks.model import AnimatedResultTask
from PIL import Image



def create_animation_text(ctx: Context, id: str):
    path = f"minecraft:block/{id}"
    render = Render(ctx, default_render_size=256)
    task = render.add_model_task(path)
    render.run()

    font: JsonDict = {
        "providers": [
            {
                "type": "reference",
                "id": "minecraft:include/space"
            }
        ]
    }
    font_path = f"{NAMESPACE}:font"

    text: list[JsonDict | str] = [""]

    char_index = 0xe000
    char_offset = 0x0004
    for i, t in enumerate(task.tasks):
        assert isinstance(t.saved_img, Image.Image)
        char_index += char_offset
        char_item = f"\\u{char_index:04x}".encode().decode("unicode_escape")

        render_path = f"{NAMESPACE}:item/font/{id}/{i}"
        ctx.assets.textures[render_path] = Texture(t.saved_img)

        font["providers"].append({
            "type": "bitmap",
            "file": f"{render_path}.png",
            "ascent": 8,
            "height": 16,
            "chars": [char_item],
        })
        text.append({
            "text": char_item + " ",
            "font": font_path,
            "color": "white",
        })
        n = 4
        if i%n == n-1:
            text.append("\n\n")

        
    ctx.assets.fonts[font_path] = Font(font)

    ctx.data[Message][f"{NAMESPACE}:{id}"] = Message(text)



def beet_default(ctx: Context):
    beet_item = Item(id="beet", item_name=(f"{NAMESPACE}:beet", {Lang.en_us: "Beet Item"})).export(ctx)


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

