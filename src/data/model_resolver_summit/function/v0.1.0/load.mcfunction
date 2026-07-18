
x = ./tick_structure_room
y = ./20tick
z = ./loop_structure

# clear scheluded functions
schedule clear x
schedule clear y
schedule clear z

# schedule function x 1t replace
# schedule function y 200t replace
# schedule function z 10t replace


execute as @e[type=item_display, tag=model_resolver_summit.beet_powered] at @s run tp @s ~ ~ ~ 0 ~


scoreboard players add #GLOBAL_SCREEN model_resolver_summit.math 0
scoreboard players set #LIGHT_STRUCTURE model_resolver_summit.math 0
scoreboard objectives add model_resolver_summit.current_display dummy

function ./load_set_max