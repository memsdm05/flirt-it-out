<script lang="ts">
import { afterUpdate, onDestroy, onMount } from "svelte";
import MessageBubble from "$/MessageBubble.svelte";

import timerStar from "$/images/timer-star.svg";

interface Message {
    fromPlayer: boolean;
    text: string;
}
let messageContainer: null | HTMLUnknownElement = null;

let messages: Message[] = [
    {fromPlayer: true, text: "hello"},
    {fromPlayer: false, text: "hello"},
    {fromPlayer: true, text: "hello"},
    {fromPlayer: false, text: "hello"},
];

let newMessageText = "";

let nSecondsRemaining = 90;
let animationHandle = 0;

let animating = false;
const startTime = Date.now();
onMount(() => {
    const onNewFrame = (now: number) => {
        nSecondsRemaining = Math.max(0, 90 - Math.floor((Date.now() - startTime) / 1000));
        animationHandle = requestAnimationFrame(onNewFrame);
    };

    animationHandle = requestAnimationFrame(onNewFrame);
    animating = true;
});
onDestroy(() => {
    clearInterval(animationHandle);
});

const send = () => {
    messages.push({
        fromPlayer: true,
        text: newMessageText.trim(),
    }, {
        fromPlayer: false,
        text: "wonderful",
    });
    messages = messages;

    newMessageText = "";
};

afterUpdate(() => {
    messageContainer?.scrollTo(0, messageContainer.scrollHeight);
});
</script>

<div class="chat-page">
    <top-bar>
        <img src="https://placehold.co/100x100" alt="Prompt" />
        
        <timer- class="strong-label">
            <!-- svelte-ignore a11y-missing-attribute -->
            <img src={timerStar}
                    class:animating={animating} />
            <span>{nSecondsRemaining}</span>
        </timer->
    </top-bar>
    
    <message-container bind:this={messageContainer}>
        {#each messages as message}
            <MessageBubble {...message} />
        {/each}
    </message-container>

    <messenger->
        <div contenteditable
                bind:innerText={newMessageText} />
    
        <button on:click={send}
                disabled={newMessageText.trim().length === 0}>Send</button>
    </messenger->
</div>

<style lang="scss">
.chat-page {
    display: flex;
    flex-flow: column;
    justify-content: space-between;
    align-items: stretch;
    gap: 1rem;
    height: 100%;
}

top-bar {
    display: flex;
    align-items: center;
    justify-content: space-around;

    > img {
        border: 0.75rem solid var(--col-yellow-light);
    }
}

timer- {
    font-size: 3rem;

    border-radius: 50%;
    aspect-ratio: 1;
    padding: 0.5rem;

    display: grid;
    place-items: center;

    > img.animating {
        animation: rotate 1s infinite cubic-bezier(.14,.54,.22,1.06);

        @keyframes rotate {
            0% {
                transform: rotate(0turn);
            }

            100% {
                transform: rotate(120deg);
            }
        }
    }

    > span {
        z-index: 1;
    }

    > * {
        grid-area: 1/1;
    }
}

message-container {
    display: flex;
    flex-flow: column;
    gap: 0.5rem;
    overflow-y: auto;
    flex-grow: 1;
    flex-shrink: 1;

    scroll-behavior: smooth;
}

messenger- {
    display: flex;
    flex-flow: column;
    gap: 1rem;
}

[contenteditable] {
    word-break: break-word;

    padding-left: 0.5em;
    padding-right: 0.5em;
}
</style>