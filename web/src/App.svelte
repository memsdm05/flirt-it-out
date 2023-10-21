<script lang="ts">
import LobbyPage from "./pages/LobbyPage.svelte";
import NamePage from "./pages/NamePage.svelte";
import QrPage from "./pages/QrPage.svelte";

import {gameId, username} from "./store";

</script>

<main>
    <h1>Flirt it out</h1>

    {#if !$gameId}
        <QrPage />
    {:else if !$username}
        <NamePage />
    {:else}
        <LobbyPage />
    {/if}
</main>

<style lang="scss">
main {
    display: flex;
    flex-flow: column;
}

h1 {
    text-transform: uppercase;
}
</style>
