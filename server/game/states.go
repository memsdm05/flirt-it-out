package game

type State interface {
	Name() string
	Start(*Room) error
	Handle(*Room /* packet */) (State, error)
}

type LobbyState struct {
}

func (l *LobbyState) Name() string {
	return "lobby"
}

func (l *LobbyState) Start(r *Room) error {
	return nil
}

func (l *LobbyState) Handle(r *Room) (State, error) {
	panic("not implemented") // TODO: Implement
}
