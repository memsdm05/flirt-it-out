import { writable } from "svelte/store";

export enum GameState {
    Lobby,
    Chat,
    Scoring,
    Leaderboard,
}
export const gameState = writable<GameState>(GameState.Chat);


export interface SocketMessage<Action extends "msg" | "anim_end"> {
    action: Action;
    payload: Action extends "msg" ? {content: string} :
            {};
}


export const socket = writable<WebSocket | null>(null);