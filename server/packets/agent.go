package packets

import (
	"sync"

	"github.com/google/uuid"
	"github.com/gorilla/websocket"
)

// TODO

type Agent struct {
	Id     uuid.UUID
	Outbox chan Packet

	once sync.Once
	done chan struct{}
}

func (a *Agent) init() {
	a.Outbox = make(chan Packet, 1)
}

func (a *Agent) consumer(conn *websocket.Conn) {

}

func (a *Agent) producer(conn *websocket.Conn) {
	for {
		select {
		case packet := <-a.Outbox:
			data, err := Marshal(packet)
			if err != nil {
				panic(err)
			}

			if conn.WriteMessage(websocket.TextMessage, data) != nil {
				panic(err)
			}
		}
	}
}

func (a *Agent) Run(conn *websocket.Conn) {
	a.once.Do(a.init)

	go a.consumer(conn)
	go a.producer(conn)
}
