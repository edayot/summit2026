tellraw @s [
    '',
    { text: 'SimpleDrawer', color: 'yellow' },
    ' is available on : ',
    {
        font: 'summit_icons:icons', 
        translate: 'summit_icons.github', 
        click_event: {
            'action': 'open_url',
            'url': 'https://github.com/edayot/SimpleDrawer'
        },
        hover_event: {
            'action': 'show_text',
            'value': 'GitHub'
        }
    },
    {
        font: 'summit_icons:icons', 
        translate: 'summit_icons.smithed', 
        click_event: {
            'action': 'open_url',
            'url': 'https://smithed.net/packs/simpledrawer'
        },
        hover_event: {
            'action': 'show_text',
            'value': 'Smithed'
        }
    },
    {
        font: 'summit_icons:icons', 
        translate: 'summit_icons.modrinth', 
        click_event: {
            'action': 'open_url',
            'url': 'https://modrinth.com/datapack/simpledrawer'
        },
        hover_event: {
            'action': 'show_text',
            'value': 'Modrinth'
        }
    },
    {
        font: 'summit_icons:icons', 
        translate: 'summit_icons.planetminecraft', 
        click_event: {
            'action': 'open_url',
            'url': 'https://www.planetminecraft.com/data-pack/simple-drawer/'
        },
        hover_event: {
            'action': 'show_text',
            'value': 'Planet Minecraft'
        }
    },
]