from beet import Context
from simple_item_plugin.types import NAMESPACE, Lang
from simple_item_plugin.item import Item, BlockProperties
from simple_item_plugin.crafting import ShapedRecipe, VanillaItem
import weld_deps


def beet_default(ctx: Context):
    beet_item = Item(id="beet", item_name=(f"{NAMESPACE}:beet", {Lang.en_us: "Beet Item"})).export(ctx)


    screen = Item(
        id="screen", 
        base_item="soul_campfire",
        item_name=(f"{NAMESPACE}:beet", {Lang.en_us: "Beet Item"}),
        block_properties=BlockProperties(
            base_block="minecraft:soul_campfire",
            block_states={
                "facing": "south",
                "lit": "false",
                "signal_fire": "true",
                "waterlogged": "false",
            },
            all_same_faces=False,
            entity_type="marker",
        ),
    ).export(ctx)
