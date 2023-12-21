package game

import (
	"encoding/json"
	"math/rand"
	"strings"

	"github.com/memsdm05/flirt-it-out/models"

	"github.com/google/uuid"
)

const (
	CodeLength = 5
)

var Rooms = make(map[string]*Room)

type chat struct {
	player  *models.Player
	bot     *models.Bot
	history []models.Message
}

type Room struct {
	Code string

	state   State
	players map[uuid.UUID]*models.Player
	host    *models.Host
	bot     *models.Bot
}

func NewRoom() *Room {
	room := &Room{
		players: make(map[uuid.UUID]*models.Player),
		state:   new(LobbyState),
	}

	room.state.Start(room)

	// Generate new code
	for {
		var sb strings.Builder
		for i := 0; i < CodeLength; i++ {
			letter := rune(rand.Intn(26)) + 'A'
			sb.WriteRune(letter)
		}
		room.Code = sb.String()
		if _, ok := Rooms[room.Code]; !ok {
			break
		}
	}

	Rooms[room.Code] = room
	return room
}

func (r *Room) NewPlayer(name string) *models.Player {
	player := &models.Player{
		Id:   uuid.Must(uuid.NewRandom()),
		Name: name,
	}
	r.players[player.Id] = player
	return player
}

func (r *Room) MarshalJSON() ([]byte, error) {
	roomProxy := struct {
		Code       string `json:"code"`
		State      string `json:"state"`
		NumPlayers int    `json:"number_of_players"`
	}{
		Code:       r.Code,
		State:      r.state.Name(),
		NumPlayers: len(r.players),
	}

	return json.Marshal(roomProxy)
}
