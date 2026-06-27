

fill ^3 ^2 ^ ^-3 ^-1 ^ oxidized_copper_bars replace air

data merge entity @s {transformation: {scale: [2.001f, 2.001f, 2.001f]}}
data merge entity @s {brightness:{block:15, sky:15}}

scoreboard players add #GLOBAL_SCREEN model_resolver_summit.math 1
scoreboard players operation @s model_resolver_summit.math = #GLOBAL_SCREEN model_resolver_summit.math


execute summon text_display run function ./place_text_display: 
    scoreboard players operation @s model_resolver_summit.math = #GLOBAL_SCREEN model_resolver_summit.math

    data merge entity @s {Tags:["model_resolver_summit.screen.text_display", "model_resolver_summit.screen.image", "summit.dynamic"], text: "", line_width: 500, background: 0}
    tag @s add model_resolver_summit.screen.part
    function model_resolver_summit:impl/set_screen_display/sculk_sensor
    tp @s ~ ~ ~ ~ ~
    execute at @s run tp @s ^1.8 ^-0.6 ^

execute summon text_display run function ./place_text_display_code: 
    scoreboard players operation @s model_resolver_summit.math = #GLOBAL_SCREEN model_resolver_summit.math

    data merge entity @s {Tags:["model_resolver_summit.screen.text_display", "model_resolver_summit.screen.code", "summit.dynamic"], text: "", line_width: 500, background: -15198184, alignment:"left"}
    tag @s add model_resolver_summit.screen.part
    function model_resolver_summit:impl/set_screen_display/sculk_sensor
    data merge entity @s {transformation: {scale: [0.6, 0.6, 0.6]}}
    tp @s ~ ~ ~ ~ ~
    execute at @s run tp @s ^-1.1 ^-0.2 ^0.025



execute summon interaction run function ./place_next_button:
    scoreboard players operation @s model_resolver_summit.math = #GLOBAL_SCREEN model_resolver_summit.math

    next_func = ~/next_structure
    prev_func = ~/prev_structure

    function next_func:
        scoreboard players add @s model_resolver_summit.current_display 1
        execute if score @s model_resolver_summit.current_display = #MAX model_resolver_summit.current_display run scoreboard players set @s model_resolver_summit.current_display 0
        function f"model_resolver_summit:impl/screen_reparts"
    function prev_func:
        scoreboard players remove @s model_resolver_summit.current_display 1
        execute if score @s model_resolver_summit.current_display matches -1 run function ~/reset:
            scoreboard players operation @s model_resolver_summit.current_display = #MAX model_resolver_summit.current_display
            scoreboard players remove @s model_resolver_summit.current_display 1
        function f"model_resolver_summit:impl/screen_reparts"

    tag @s add summit.interactable
    tag @s add model_resolver_summit.screen.part
    data merge entity @s {
        width: 6,
        height: 3.25,
        data: {summit_interactable: {
            on_right_click: f"function {next_func}",
            on_left_click: f"function {prev_func}",
        }}
    }
    tp @s ~ ~ ~ ~ ~
    execute at @s run tp @s ^0 ^-1 ^-2.8

