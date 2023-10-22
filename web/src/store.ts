import { writable } from "svelte/store";

export enum GameState {
    Lobby,
    Chat,
    Scoring,
    Leaderboard,
}
export const gameState = writable<GameState>(GameState.Lobby);

export const roundEnd = writable<Date>(new Date());
export const botName = writable<string>("");


export type SocketMessageAction = "msg" | "stasis" | "start_round";
export interface SocketMessage<Action extends SocketMessageAction=SocketMessageAction> {
    action: Action;
    payload: Action extends "msg" ? {content: string} :
            Action extends "stasis" ? {display: string} :
            Action extends "start_round" ? {ends_at: string, bot_name: string} :
            {};
}

export const socket = writable<WebSocket | null>(null);