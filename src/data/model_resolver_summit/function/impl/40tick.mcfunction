schedule function ~/ 40t replace


execute as @e[tag=model_resolver_summit.beet_powered, type=item_display] at @s run function ~/beet_powered:

    execute store success score #temp model_resolver_summit.math if entity @s[tag=model_resolver_summit.beet_powered.switch]

    execute if score #temp model_resolver_summit.math matches 1 run function ~/switch:
        tp @s ~ ~ ~ 360 ~
        tag @s remove model_resolver_summit.beet_powered.switch

    execute if score #temp model_resolver_summit.math matches 0 run function ~/noswitch:
        tp @s ~ ~ ~ 180 ~
        tag @s add model_resolver_summit.beet_powered.switch

    






