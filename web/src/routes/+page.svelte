<script lang="ts">
import {onMount} from "svelte";

import LobbyPage from "$/pages/LobbyPage.svelte";
import ChatPage from "$/pages/ChatPage.svelte";
import DrumrollPage from "$/pages/DrumrollPage.svelte";

import {GameState, gameState, socket} from "@/store";


onMount(() => {
    const socketUrl = new URL("/client", location.href);
    socketUrl.protocol = socketUrl.protocol.replace("http", "ws");
    $socket = new WebSocket(socketUrl.href);
    $socket.addEventListener("open", () => {
        console.log("socket ready");
    });
})
</script>

{#if $gameState === GameState.Lobby}
    <LobbyPage />
{:else if $gameState === GameState.Chat}
    <ChatPage />
{:else}
    <DrumrollPage />
{/if}