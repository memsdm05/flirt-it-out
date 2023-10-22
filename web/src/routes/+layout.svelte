<script lang="ts">
import starburst from "$/images/starburst.svg";
import heartsBottom from "$/images/hearts-bottom.svg";

import "@/app.scss";
</script>

<main>
    <img src={starburst} class="starburst" alt="Starburst" />
    <img src={heartsBottom} class="hearts-bottom" alt="Starburst" />

    <header>
        <h1>Flirt it Out</h1>
    </header>

    <slot />
</main>

<style lang="scss">
main {
    width: 100vw;
    height: 100vh;

    display: grid;
    grid-template-rows: 8rem 1fr 8rem;
    align-items: center;
    justify-items: center;

    text-align: center;

    overflow: hidden;

    > :global(:not(img)) {
        z-index: 1;
    }

    > .starburst {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);

        height: calc(100vh - 16rem);
    }

    > .hearts-bottom {
        position: absolute;
        left: 50%;
        transform: translate(-50%, 0);
        bottom: 0;
    }

    > :global(div) {
        display: flex;
        flex-flow: column;
        align-items: center;
        width: 100%;
        flex-grow: 1;
        padding: 0 2rem;
        max-width: 390px;
    }

    > :global(.chat-page) {
        grid-row: 2 / 4;
    }
}

h1 {
    text-transform: uppercase;
    z-index: 1;
    text-shadow: 0 0 1rem var(--col-red),
        1px 1px var(--col-yellow),
        2px 2px var(--col-yellow),
        3px 3px var(--col-yellow),
        4px 4px var(--col-yellow),
        4px 4px 1rem #861524,
        4px 4px 0.5rem #861524;

    transform: skewY(-4deg) skewX(-4deg);
}
</style>
