package models

import "github.com/google/uuid"

func init() {

}

type Player struct {
	Id   uuid.UUID
	Name string
}
