<script lang="ts">
import { cubicOut } from "svelte/easing";
import { fade, type TransitionConfig } from "svelte/transition";

export let text: string;
export let fromPlayer: boolean;

export let awaiting = false;
export let hasSendingIndicator = false;
export let hasReceivedIndicator = false;
</script>

<div class:from-player={fromPlayer}
        class:awaiting={awaiting}
        in:fade={{duration: 500, easing: cubicOut}}
        class="message-bubble">
    {#if !awaiting}
        {text}
    {:else}
        <div class="ellipsis"></div>
        <div class="ellipsis dot-2"></div>
        <div class="ellipsis dot-3"></div>
    {/if}

    {#if hasSendingIndicator}
        <div class="sending-indicator"
                transition:fade={{duration: 200, easing: cubicOut}}>Sending…</div>
    {/if}

    {#if hasReceivedIndicator}
        <div class="sending-indicator"
                transition:fade={{duration: 200, easing: cubicOut}}>Received!</div>
    {/if}
</div>

<style lang="scss">
.message-bubble {
    max-width: 70%;
    padding: 0.5rem;
    align-self: flex-start;
    display: flex;
    flex-flow: row;
    gap: 0.5rem;
    position: relative;

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

    &.awaiting {
        padding: 1rem;
    }
}


.sending-indicator {
    align-self: flex-end;
    font-size: 1rem;
    position: absolute;
    right: 100%;
    bottom: 0;
    width: 30ch;
    margin-right: 0.5rem;
    color: #fff;
}

.ellipsis {
    background: var(--col-red);
    width: 0.5rem;
    aspect-ratio: 1;

    border-radius: 50%;

    animation: ellipsis-bounce 2s infinite;

    @keyframes ellipsis-bounce {
        0% {
            transform: scale(1, 1);
        }

        20% {
            transform: translateY(4px) scale(2, 0.5);
        }

        40% {
            transform: translateY(-8px) scale(0.4, 2.5);
        }

        60% {
            transform: translateY(4px) scale(1.5, 0.6666666);
        }

        80% {
            transform: scale(1,1);
        }
    }

    &.dot-2 {
        animation-delay: 0.25s;
    }

    &.dot-3 {
        animation-delay: 0.5s;
    }
}
</style>