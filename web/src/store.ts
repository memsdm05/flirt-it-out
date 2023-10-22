import { writable } from "svelte/store";

export enum GameState {
    Lobby,
    Chat,
    Scoring,
    Leaderboard,
}
export const gameState = writable<GameState>(GameState.Lobby);


export interface SocketMessage<Action extends "msg" | "stasis"> {
    action: Action;
    payload: Action extends "msg" ? {content: string} :
            Action extends "stasis" ? {display: string} :
            {};
}


export const socket = writable<WebSocket | null>(null);