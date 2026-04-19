

execute as @a[tag=convention.debug] run function model_resolver_summit:impl/print_version
schedule function ./tick 1t replace


scoreboard players add #GLOBAL_SCREEN model_resolver_summit.math 0
