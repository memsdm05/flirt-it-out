package game

import (
	"encoding/json"
	"math/rand"
	"strings"
	"sync"

	"github.com/memsdm05/flirt-it-out/models"

	"github.com/google/uuid"
)

const (
	CodeLength = 5
)

var Rooms = make(map[string]*Room)

type chat struct {
	player  *Player
	bot     *Bot
	history []models.Message
}

type Room struct {
	Code string

	sync.Mutex
	state   State
	players map[uuid.UUID]*Player
	host    *Host
	bot     *Bot
}

func NewRoom() *Room {
	room := &Room{
		players: make(map[uuid.UUID]*Player),
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

func (r *Room) NewPlayer(name string) *Player {
	r.Lock()
	defer r.Unlock()

	player := &Player{
		Name: name,
	}
	player.Id = uuid.Must(uuid.NewRandom())

	r.players[player.Id] = player
	return player
}

func (r *Room) NewHost() *Host {
	r.Lock()
	defer r.Unlock()

	if r.host != nil {
		return nil
	}
	// TODO implement more rebust host check

	host := &Host{}
	host.Id = uuid.Nil

	r.host = host
	return host
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
