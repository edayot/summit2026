

fill ^3 ^2 ^ ^-3 ^-1 ^ oxidized_copper_bars replace air

data merge entity @s {transformation: {scale: [2.001f, 2.001f, 2.001f]}}
data merge entity @s {brightness:{block:15, sky:15}}

scoreboard players add #GLOBAL_SCREEN model_resolver_summit.math 1
scoreboard players operation @s model_resolver_summit.math = #GLOBAL_SCREEN model_resolver_summit.math


execute summon text_display run function ./place_text_display: 
    scoreboard players operation @s model_resolver_summit.math = #GLOBAL_SCREEN model_resolver_summit.math

    data merge entity @s {Tags:["model_resolver_summit.screen.text_display", "model_resolver_summit.screen.image", "summit.dynamic"], text: "", line_width: 500, background: 0}
    function model_resolver_summit:impl/set_screen_display/sculk_sensor
    tp @s ~ ~ ~ ~ ~
    execute at @s run tp @s ^1.8 ^-0.6 ^

execute summon text_display run function ./place_text_display_code: 
    scoreboard players operation @s model_resolver_summit.math = #GLOBAL_SCREEN model_resolver_summit.math

    data merge entity @s {Tags:["model_resolver_summit.screen.text_display", "model_resolver_summit.screen.code", "summit.dynamic"], text: "", line_width: 500, background: -15198184, alignment:"left"}
    function model_resolver_summit:impl/set_screen_display/sculk_sensor
    data merge entity @s {transformation: {scale: [0.6, 0.6, 0.6]}}
    tp @s ~ ~ ~ ~ ~
    execute at @s run tp @s ^-1.1 ^-0.2 ^0.025




# summon interaction ~ ~ ~ {Tags: ["summit.interactable"], data: {summit_interactable: {on_right_click: "execute on target run function a:bc"}}}

