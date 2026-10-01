CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  age INTEGER NOT NULL CHECK (age >= 0),
  sex TEXT NOT NULL CHECK (sex IN ('male', 'female')),
  weight REAL NOT NULL CHECK (weight > 0),
  height REAL NOT NULL CHECK (height > 0)
);

CREATE TABLE IF NOT EXISTS targets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    energy REAL NOT NULL CHECK (energy > 0),                         -- kcal/day
    protein REAL NOT NULL CHECK (protein >= 0),                     -- g/day
    fatty_acids REAL NOT NULL CHECK (fatty_acids >= 0),             -- g/day
    saturated_fatty_acids REAL NOT NULL CHECK (saturated_fatty_acids >= 0), -- g/day
    carbohydrates REAL NOT NULL CHECK (carbohydrates >= 0),         -- g/day
    fibre REAL NOT NULL CHECK (fibre >= 0),                         -- g/day
    pal REAL NOT NULL CHECK (pal > 0),                              -- dimensionless

    FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS nutritional_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,

    energy REAL NOT NULL DEFAULT 0 CHECK (energy >= 0),                    -- kcal/100 g
    protein REAL NOT NULL DEFAULT 0 CHECK (protein >= 0),                  -- g/100 g
    fatty_acids REAL NOT NULL DEFAULT 0 CHECK (fatty_acids >= 0),          -- g/100 g
    saturated_fatty_acids REAL NOT NULL DEFAULT 0 CHECK (saturated_fatty_acids >= 0), -- g/100 g
    carbohydrates REAL NOT NULL DEFAULT 0 CHECK (carbohydrates >= 0),      -- g/100 g
    fibre REAL NOT NULL DEFAULT 0 CHECK (fibre >= 0),                      -- g/100 g

    protein_digestibility REAL NOT NULL DEFAULT 0 CHECK (protein_digestibility >= 0),

    calcium REAL NOT NULL DEFAULT 0 CHECK (calcium >= 0),                  -- mg/100 g
    iodine REAL NOT NULL DEFAULT 0 CHECK (iodine >= 0),                    -- µg/100 g
    selenium REAL NOT NULL DEFAULT 0 CHECK (selenium >= 0),                -- µg/100 g
    phosphorus REAL NOT NULL DEFAULT 0 CHECK (phosphorus >= 0),            -- mg/100 g

    isoleucine REAL NOT NULL DEFAULT 0 CHECK (isoleucine >= 0),            -- mg/100 g
    leucine REAL NOT NULL DEFAULT 0 CHECK (leucine >= 0),                  -- mg/100 g
    lysine REAL NOT NULL DEFAULT 0 CHECK (lysine >= 0),                    -- mg/100 g
    methionine REAL NOT NULL DEFAULT 0 CHECK (methionine >= 0),            -- mg/100 g
    phenylalanine REAL NOT NULL DEFAULT 0 CHECK (phenylalanine >= 0),      -- mg/100 g
    threonine REAL NOT NULL DEFAULT 0 CHECK (threonine >= 0),              -- mg/100 g
    tryptophan REAL NOT NULL DEFAULT 0 CHECK (tryptophan >= 0),            -- mg/100 g
    valine REAL NOT NULL DEFAULT 0 CHECK (valine >= 0),                    -- mg/100 g
    histidine REAL NOT NULL DEFAULT 0 CHECK (histidine >= 0),              -- mg/100 g

    folic_acid REAL NOT NULL DEFAULT 0 CHECK (folic_acid >= 0),            -- µg/100 g
    natrium REAL NOT NULL DEFAULT 0 CHECK (natrium >= 0),                  -- mg/100 g
    vitamin_b6 REAL NOT NULL DEFAULT 0 CHECK (vitamin_b6 >= 0),             -- µg/100 g
    vitamin_b12 REAL NOT NULL DEFAULT 0 CHECK (vitamin_b12 >= 0)            -- µg/100 g
);
