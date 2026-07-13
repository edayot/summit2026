schedule function ~/ 4t replace


BLOCK_ON  = "minecraft:copper_bulb[lit=true]"
BLOCK_OFF = "minecraft:copper_bulb[lit=false]"

base_pos = [195, 93, -4]

states = [
    "000111000",
    "000011100",
    "000001110",
    "000000111",
    "100000011",
    "110000001",
    "111000000",
    "011100000",
    "001110000",
]
scoreboard players add #LIGHT_STRUCTURE model_resolver_summit.math 1
execute if score #LIGHT_STRUCTURE model_resolver_summit.math matches f"{len(states)}.." run scoreboard players set #LIGHT_STRUCTURE model_resolver_summit.math 0


for i, state in enumerate(states):
    execute 
        if score #LIGHT_STRUCTURE model_resolver_summit.math matches f"{i}" 
        run function f"model_resolver_summit:v0.1.0/place_state/{i}":
            for j in range(9):
                pos_1 = f"{base_pos[0] + j} {base_pos[1]} {base_pos[2]}"
                pos_2 = f"{base_pos[0] + j} {base_pos[1]} {base_pos[2]+2}"
                if state[j] == "1":
                    block = BLOCK_ON
                else:
                    block = BLOCK_OFF
                raw f"setblock {pos_1} {block}"
                raw f"setblock {pos_2} {block}"
