<script lang="ts">
export let text: string;
export let fromPlayer: boolean;
</script>

<div class:from-player={fromPlayer}>
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