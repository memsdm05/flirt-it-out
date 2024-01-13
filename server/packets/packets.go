package packets

import "encoding/json"

type AgentType int

const (
	None = AgentType(iota)
	Client
	Host
)

type Packet interface {
	Action() string
	Producer() AgentType
	Consumer() AgentType
}

func Marshal(packet Packet) ([]byte, error) {
	raw := struct {
		Action  string `json:"action"`
		Payload any    `json:"payload"`
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

func (Message) Action() string      { return "msg" }
func (Message) Producer() AgentType { return Client }
func (Message) Consumer() AgentType { return Client }

type Kick struct {
	Reason string `json:"reason"`
}

func (Kick) Action() string      { return "kick" }
func (Kick) Producer() AgentType { return None }
func (Kick) Consumer() AgentType { return Client | Host }
