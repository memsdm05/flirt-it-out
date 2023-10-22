<script lang="ts">
import { cubicOut } from "svelte/easing";
import { fade, type TransitionConfig } from "svelte/transition";

export let text: string;
export let fromPlayer: boolean;
</script>

<div class:from-player={fromPlayer}
        in:fade={{duration: 500, easing: cubicOut}}>
    {text}
</div>

<style lang="scss">
div {
    max-width: 80%;
    padding: 0.5rem;
    align-self: flex-start;

    background: var(--col-yellow-light);
    text-align: left;
    color: var(--col-red);

    border-radius: 1rem;
    font-size: 1.25rem;
    word-break: break-word;

    &:not(.from-player) {
        border-bottom-left-radius: 0;
    }

    &.from-player {
        align-self: flex-end;

        text-align: right;
        background: #fff;

        border-bottom-right-radius: 0;
    }
}
</style>