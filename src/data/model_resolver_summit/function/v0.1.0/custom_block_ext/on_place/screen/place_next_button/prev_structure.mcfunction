execute on attacker run playsound minecraft:entity.glow_item_frame.rotate_item block @a[distance=..10] ~ ~ ~ 2 1
scoreboard players remove @s model_resolver_summit.current_display 1
execute if score @s model_resolver_summit.current_display matches -1 run function model_resolver_summit:v0.1.0/custom_block_ext/on_place/screen/place_next_button/prev_structure/reset
function model_resolver_summit:v0.1.0/screen_reparts
