tellraw @s [
    '',
    'The code is on ',
    {
        font: 'summit_icons:icons', 
        translate: 'summit_icons.github', 
        click_event: {
            'action': 'open_url',
            'url': 'https://github.com/edayot/model_resolver'
        },
        hover_event: {
            'action': 'show_text',
            'value': 'GitHub'
        }
    },
]