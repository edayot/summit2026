from beet import Context
from simple_item_plugin.types import NAMESPACE, Lang
from simple_item_plugin.item import Item, BlockProperties
from simple_item_plugin.crafting import ShapedRecipe, VanillaItem


def beet_default(ctx: Context):
    beet_item = Item(id="beet", item_name=(f"{NAMESPACE}:beet", {Lang.en_us: "Beet Item"})).export(ctx)


    screen = Item(
        id="screen", 
        base_item="furnace",
        item_name=(f"{NAMESPACE}:screen", {Lang.en_us: "Screen"}),
        block_properties=BlockProperties(
            base_block="minecraft:oxidized_copper_bars",
            entity_type="item_display",
        ),
    ).export(ctx)
