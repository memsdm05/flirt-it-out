<script lang="ts">
import ChatPage from "$/pages/ChatPage.svelte";
import LobbyPage from "$/pages/LobbyPage.svelte";
import NamePage from "$/pages/NamePage.svelte";
import QrPage from "$/pages/QrPage.svelte";

import {gameId, username} from "../store";

</script>

{#if !$gameId}
    <QrPage />
{:else if !$username}
    <NamePage />
{:else}
    <!-- <LobbyPage /> -->
    <ChatPage />
{/if}