import { writable } from "svelte/store";

export enum GameState {
    Lobby,
    Chat,
    Scoring,
    Leaderboard,
}
export const gameState = writable<GameState>(GameState.Chat);