execute on target run playsound minecraft:entity.glow_item_frame.rotate_item block @a ~ ~ ~ 2 1
scoreboard players add @s model_resolver_summit.current_display 1
execute if score @s model_resolver_summit.current_display = #MAX model_resolver_summit.current_display run scoreboard players set @s model_resolver_summit.current_display 0
function model_resolver_summit:v0.1.0/screen_reparts
