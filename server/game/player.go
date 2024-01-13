package game

import (
	"github.com/memsdm05/flirt-it-out/packets"
)

type Player struct {
	packets.Agent
	Name string
}
