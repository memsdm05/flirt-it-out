<script lang="ts">
import LobbyPage from "$/pages/LobbyPage.svelte";
import ChatPage from "$/pages/ChatPage.svelte";
import DrumrollPage from "@/lib/pages/DrumrollPage.svelte";

import {GameState, gameState} from "@/store";
</script>

{#if $gameState === GameState.Lobby}
    <LobbyPage />
{:else if $gameState === GameState.Chat}
    <ChatPage />
{:else}
    <DrumrollPage />
{/if}