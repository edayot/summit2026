
# clear scheluded functions
schedule clear ./tick_structure_room
schedule clear ./20tick
schedule clear ./loop_structure

# schedule function ./tick_structure_room 1t replace
# schedule function ./20tick 200t replace
# schedule function ./loop_structure 10t replace


execute as @e[tag=model_resolver_summit.beet_powered, type=item_display] at @s run tp @s ~ ~ ~ 0 ~


scoreboard players add #GLOBAL_SCREEN model_resolver_summit.math 0
scoreboard players set #LIGHT_STRUCTURE model_resolver_summit.math 0
scoreboard objectives add model_resolver_summit.current_display dummy

function ./load_set_max