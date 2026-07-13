execute store result score #temp model_resolver_summit.math if entity @a[tag=summit.in_booth.model_resolver_summit]

execute 
    if score #temp model_resolver_summit.math matches 1 
    summon item_display
    run function ~/replace_book:
        setblock 208 95 -20 lectern[facing=west,has_book=true,powered=false]
        data modify block 208 95 -20 Page set value 0
        loot replace entity @s container.0 loot model_resolver_summit:guide
        data modify block 208 95 -20 Book set from entity @s item
        kill @s

