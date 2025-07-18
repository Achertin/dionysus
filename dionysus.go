package main

import (
	"database/sql"
	_ "github.com/mattn/go-sqlite3"
	"log"
	"fmt"
)

const USER = "alka"
const RECIPE = "ranajky bratislava"

type target struct {
	energy float64
	protein float64
	fatty_acids float64
	carbohydrates float64
	fibre float64
}

func get_target(db *sql.DB) (*target, error) {
	sql := `SELECT energy, protein, fatty_acids, carbohydrates, fibre 
			FROM targets WHERE name='` + USER + "'"
	row := db.QueryRow(sql)
	c := &target{}
	err := row.Scan(&c.energy, &c.protein, &c.fatty_acids, &c.carbohydrates, &c.fibre)
	if err != nil {
		return nil, err
	}
	return c, nil
}
func main() {
	db, err := sql.Open("sqlite3", "./food.db")
	if err != nil {
		log.Fatal(err)
	}
	
	test_query, err := get_target(db)
	if err != nil {
		log.Fatal(err)
	}

	fmt.Printf("%+v", *test_query)
	defer db.Close()
}
