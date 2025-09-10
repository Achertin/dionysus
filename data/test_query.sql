SELECT DISTINCT recipes.recipe_name FROM recipes
LEFT JOIN targets ON recipes.user_id=targets.id
WHERE targets.name = 'luki'
