data merge entity @s {transformation: {scale: [2.001f, 2.001f, 2.001f]}}

execute summon text_display run function ./place_text_display: 
    res = ""
    for i in range(12):
        res = res + (chr(65+i)) * 37 + "\n"
    res = res[:-1]

    data merge entity @s {Tags:["model_resolver_summit.screen.text_display"], text: res, line_width: 500, background: 0}
    tp @s ~ ~-0.8 ~ ~ ~