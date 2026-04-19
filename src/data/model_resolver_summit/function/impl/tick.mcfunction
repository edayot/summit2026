schedule function ~/ 1t replace



# @to_remove
execute 
    as @e[tag=model_resolver_summit.screen]
    at @s
    function ./check_air:
        scoreboard players set #destroy model_resolver_summit.math 0
        for i in range(-3, 4, 1):
            for j in range(-1, 3, 1):
                execute unless block ^i ^j ^ oxidized_copper_bars run scoreboard players set #destroy model_resolver_summit.math 1


        execute if score #destroy model_resolver_summit.math matches 1 run function ./destroy_screen:
            fill ^3 ^2 ^ ^-3 ^-1 ^ air replace oxidized_copper_bars
            scoreboard players operation #SEARCH_ID model_resolver_summit.math = @s model_resolver_summit.math 
            kill @e[type=text_display, tag=model_resolver_summit.screen.text_display, distance=..4, predicate=model_resolver_summit:impl/search_id]
            kill @s
