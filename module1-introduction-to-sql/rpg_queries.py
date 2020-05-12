import sqlite3

-- How many total Characters are there? (302 total characters)

SELECT count(distinct character_id) as total_chars
FROM charactercreator_character

-- How many of each specific subclass?
-- Clerics: (75 total characters)

SELECT count(distinct character_ptr_id) as chars_cleric
FROM charactercreator_cleric

-- Fighter: (68 total characters)

SELECT count(distinct character_ptr_id) as chars_fighter
FROM charactercreator_fighter

-- Mage:(97 total characters)

SELECT count(distinct character_ptr_id) as chars_mage
FROM charactercreator_mage
WHERE character_ptr_id >= 69 AND character_ptr_id <= 165

-- Necromancer: (11 total characters)

SELECT count(distinct mage_ptr_id) as chars_necromancer
FROM charactercreator_necromancer

-- Thief: (51 total characters)

SELECT count(distinct character_ptr_id) as chars_thief
FROM charactercreator_thief

--How many total Items? (174 total items)

SELECT count(distinct item_id) as total_items
FROM armory_item

/*How many of the Items are weapons? How many are not? (37 are weapons,
137 are not)*/

SELECT count(distinct item ptr_id) as total_weapons
FROM armory_weapon

SELECT count(distinct item_id) as total_non_weapons
FROM armory_item
LEFT JOIN armory_weapon on armory_item.item_id = armory_weapon.item_ptr_id
WHERE armory_weapon.power IS NULL

--How many Items does each character have? (Return first 20 rows)

SELECT 
	character_id
	,count(armory_item.item_id) AS total_non_weapons
FROM armory_item
LEFT JOIN charactercreator_character_inventory on charactercreator_character_inventory.item_id = armory_item.item_id
LEFT JOIN armory_weapon on armory_weapon.item_ptr_id = armory_item.item_id
WHERE armory_weapon.item_ptr_id IS NULL
GROUP BY character_id
ORDER BY character_id
LIMIT 20

--How many Weapons does each character have? (Return first 20 rows)

SELECT 
	character_id
	,count(distinct armory_weapon.item_ptr_id) as total_weapons
FROM armory_weapon
JOIN  charactercreator_character_inventory on charactercreator_character_inventory.item_id = armory_item.item_id
JOIN armory_item on armory_item.item_id = armory_weapon.item_ptr_id
GROUP BY charactercreator_character_inventory.character_id
ORDER BY charactercreator_character_inventory.character_id
LIMIT 20

--On average, how many Items does each Character have? (2.4386)

SELECT
	avg(total_non_weapons)
FROM (
	SELECT 
		character_id
		,count(armory_item.item_id) AS total_non_weapons
	FROM armory_item
	LEFT JOIN charactercreator_character_inventory on charactercreator_character_inventory.item_id = armory_item.item_id
	LEFT JOIN armory_weapon on armory_weapon.item_ptr_id = armory_item.item_id
	WHERE armory_weapon.item_ptr_id IS NULL
	GROUP BY character_id
	ORDER BY character_id

--On average, how many Weapons does each character have? (1.3097)

SELECT
	avg(total_weapons)
FROM (
	SELECT 
		character_id
		,count(distinct armory_weapon.item_ptr_id) as total_weapons
	FROM armory_weapon
	JOIN  charactercreator_character_inventory on charactercreator_character_inventory.item_id = armory_item.item_id
	JOIN armory_item on armory_item.item_id = armory_weapon.item_ptr_id
	GROUP BY charactercreator_character_inventory.character_id
	ORDER BY charactercreator_character_inventory.character_id
)
