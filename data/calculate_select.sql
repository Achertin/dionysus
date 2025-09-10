SELECT nutritional_data.*, 
(nutritional_data.protein * nutritional_data.protein_digestibility) AS protein,
recipes.minimum, recipes.maximum
FROM nutritional_data 
LEFT JOIN recipes
ON nutritional_data.id=recipes.food_id 
LEFT JOIN targets
ON recipes.user_id=targets.id
WHERE recipes.recipe_name='ranajky bratislava'
AND targets.name = 'alka';
