import { writable } from "svelte/store";

export enum GameState {
    Lobby,
    Chat,
    Scoring,
    Leaderboard,
}
export const gameState = writable<GameState>(GameState.Chat);

export const roundEnd = writable<Date>(new Date());
export const botName = writable<string>("");


export type SocketMessageAction = "msg" | "stasis" | "start_round";
export interface SocketMessage {
    action: SocketMessageAction;
    payload: string;
}

export type SocketPayload<Action extends SocketMessageAction=SocketMessageAction> =
        Action extends "msg" ? {content: string} :
        Action extends "stasis" ? {display: string} :
        Action extends "start_round" ? {ends_at: string, bot_name: string} :
        {};

export const socket = writable<WebSocket | null>(null);