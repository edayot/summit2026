

execute as @a[tag=convention.debug] run function model_resolver_summit:impl/print_version
schedule function ./tick 1t replace
schedule function ./40tick 40t replace
schedule function ./200tick 200t replace


scoreboard players add #GLOBAL_SCREEN model_resolver_summit.math 0
