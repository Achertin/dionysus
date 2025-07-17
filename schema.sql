CREATE TABLE IF NOT EXISTS targets (
	id INTEGER,
	name TEXT NOT NULL,
	energy FLOAT NOT NULL CHECK (energy>0),
	protein FLOAT NOT NULL CHECK (protein>0),
	fatty_acids FLOAT NOT NULL CHECK (fatty_acids>0),
	carbohydrates FLOAT NOT NULL CHECK (carbohydrates>0),
	fibre FLOAT NOT NULL CHECK (fibre>0),
	PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS nutritional_data (
	id INTEGER,
	food TEXT UNIQUE,
	energy FLOAT CHECK (energy>=0),
	protein FLOAT CHECK (protein>=0),
	fatty_acids FLOAT CHECK (fatty_acids>=0),
	saturated_fatty_acids FLOAT CHECK (saturated_fatty_acids>=0),
	carbohydrates FLOAT CHECK (carbohydrates>=0),
	fibre FLOAT CHECK (fibre>=0),
	calcium FLOAT CHECK (calcium>=0),
	PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS recipes (
	user_id INTEGER,
	recipe_name TEXT NOT NULL,
	food_id INTEGER,
	minimum FLOAT CHECK (minimum>=0),
	maximum FLOAT CHECK (maximum>=0),
	FOREIGN KEY(user_id) REFERENCES targets(id),
	FOREIGN KEY (food_id) REFERENCES nutritional_data(id)
);
