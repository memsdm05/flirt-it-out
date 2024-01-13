package models

import "github.com/google/uuid"

type Message struct {
	Sender uuid.UUID
	Content string 
}
