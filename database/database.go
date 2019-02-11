/*
 * database.go
 * ATOM
 *
 * Created by Karthik V
 * Created on Sat Feb 09 2019 4:30:02 PM
 *
 * Copyright © 2019 Karthik Venkatesh. All rights reserved.
 */

package database

import (
	"database/sql"
	"fmt"

	"github.com/ATOM/utills"
	_ "github.com/mattn/go-sqlite3"
)

type SQLiteManager struct {
	DB *sql.DB
}

func NewSQLiteManager() *SQLiteManager {
	sm := SQLiteManager{}
	sm.createDatabase()
	return &sm
}

func (s *SQLiteManager) createDatabase() {
	db, err1 := sql.Open("sqlite3", utills.DatabasePath())
	if err1 != nil {
		fmt.Println("Database Error: ", err1.Error())
	}
	s.DB = db
	statement, _ := db.Prepare("CREATE TABLE IF NOT EXISTS label (id INTEGER PRIMARY KEY, name TEXT)")
	_, err2 := statement.Exec()
	if err2 != nil {
		fmt.Println("Database Error: ", err2.Error())
	}
}

func (s *SQLiteManager) addLabel(label string) (*int64, error) {
	query := fmt.Sprintf("INSERT INTO label (name) values ('%s')", label)
	result, err := s.DB.Exec(query)
	if err != nil {
		fmt.Println("Database Error: ", err.Error())
		return nil, err
	}
	id, err := result.LastInsertId()
	if err != nil {
		fmt.Println("Database Error: ", err.Error())
		return nil, err
	}
	return &id, nil
}

func (s *SQLiteManager) IdForLabel(label string) (*int64, error) {
	query := fmt.Sprintf("SELECT * FROM label WHERE name='%s'", label)
	rows, err := s.DB.Query(query)
	if err != nil {
		fmt.Println("Database Error: ", err.Error())
		return nil, err
	}

	var id int64 = -1
	var name string = ""

	for rows.Next() {
		rows.Scan(&id, &name)
	}
	if id == -1 && name == "" {
		latInsertedId, err := s.addLabel(label)
		id = *latInsertedId
		fmt.Println(id)
		fmt.Println(err)
	}
	return &id, err
}
