import { writable } from "svelte/store";

export const gameId = writable<string | null>(null);
export const username = writable<string | null>(null);