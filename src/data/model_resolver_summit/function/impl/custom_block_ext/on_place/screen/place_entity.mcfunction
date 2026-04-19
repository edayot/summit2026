
from beet.contrib.messages import Message

data merge entity @s {transformation: {scale: [2.001f, 2.001f, 2.001f]}}

execute summon text_display run function ./place_text_display: 

    text = ctx.data[Message]["model_resolver_summit:sculk_sensor"].data
    data merge entity @s {Tags:["model_resolver_summit.screen.text_display"], text: text, line_width: 500, background: 0}
    tp @s ~ ~-0.8 ~ ~ ~