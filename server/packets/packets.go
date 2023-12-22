package packets

import "encoding/json"

type Agent int

const (
	None = Agent(iota)
	Client
	Host
)

type Packet interface {
	Action() string
	Producer() Agent
	Consumer() Agent
}

func Marshal(packet Packet) ([]byte, error) {
	raw := struct {
		Action  string `json:"action"`
		Payload Packet `json:"packet"`
	}{
		Action:  packet.Action(),
		Payload: packet,
	}

	return json.Marshal(raw)
}

func Unmarshal(data []byte) (Packet, error) {
	var raw struct {
		Action  string          `json:"action"`
		Payload json.RawMessage `json:"packet"`
	}

	err := json.Unmarshal(data, &raw)
	if err != nil {
		return nil, err
	}

	var p Packet
	switch raw.Action {
	case "msg":
		p = new(Message)
	}

	return p, json.Unmarshal(raw.Payload, &p)
}

type Message struct {
	Source  string `json:"source"`
	Content string `json:"content"`
}

func (Message) Action() string  { return "msg" }
func (Message) Producer() Agent { return Client }
func (Message) Consumer() Agent { return Client }

type Kick struct {
	Reason string `json:"reason"`
}

func (Kick) Action() string  { return "kick" }
func (Kick) Producer() Agent { return None }
func (Kick) Consumer() Agent { return Client | Host }
