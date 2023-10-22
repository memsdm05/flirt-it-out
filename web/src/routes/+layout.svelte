<script lang="ts">
import starburst from "$/images/starburst.svg";

import "@/app.scss";
</script>

<main>
    <img src={starburst} alt="Starburst" />

    <header>
        <h1>Flirt it Out</h1>
    </header>

    <slot />
</main>

<style lang="scss">
main {
    width: 100%;
    height: 100vh;

    display: grid;
    grid-template-rows: 8rem 1fr 8rem;
    align-items: center;

    text-align: center;

    overflow: hidden;

    > img {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
    }

    > :global(div) {
        display: flex;
        flex-flow: column;
        align-items: center;
        width: 100%;
        flex-grow: 1;
        padding: 2rem;
        overflow: hidden;
        z-index: 1;
    }

    > :global(.chat-page) {
        grid-row: 2 / 4;
    }
}

h1 {
    text-transform: uppercase;
    z-index: 1;
}
</style>