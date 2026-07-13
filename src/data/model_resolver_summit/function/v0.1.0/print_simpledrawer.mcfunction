

links = [
    ("GitHub", "https://github.com/edayot/SimpleDrawer", "summit_icons.github"),
    ("Smithed", "https://smithed.net/packs/simpledrawer", "summit_icons.smithed"),
    ("Modrinth", "https://modrinth.com/datapack/simpledrawer", "summit_icons.modrinth"),
    ("Planet Minecraft", "https://www.planetminecraft.com/data-pack/simple-drawer/", "summit_icons.planetminecraft"),
]

actions = []
for link in links:
    actions.append({
        "label": [
            "", 
            {
                "font": 'summit_icons:icons', 
                "translate": link[2],
            }, 
            " ",
            link[0]
        ],
        "tooltip": {"text": link[1], "color": "gray"},
        "width": 300,
        "action": {"type": "open_url", "url": link[1]},
    })


dialog show @s {
    "type": "minecraft:multi_action",
    "title": {"text": "Links", "bold": True, "color": "#FFD479"},
    "body": [],
    "columns": 1,
    "actions": actions,
    "exit_action": {"label": {"text": "Close", "color": "red"}},
    "can_close_with_escape": True,
}
