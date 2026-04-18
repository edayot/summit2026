from beet import Context
from simple_item_plugin.types import NAMESPACE, Lang
from simple_item_plugin.item import Item
from simple_item_plugin.crafting import ShapedRecipe, VanillaItem


def beet_default(ctx: Context):
    beet_item = Item(id="beet", item_name=(f"{NAMESPACE}:beet", {Lang.en_us: ""})).export(ctx)
