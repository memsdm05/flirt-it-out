<script lang="ts">
import { afterUpdate, onDestroy, onMount, tick } from "svelte";
import { fly } from "svelte/transition";
import { cubicOut } from "svelte/easing";
import MessageBubble from "$/MessageBubble.svelte";

import timerStar from "$/images/timer-star.svg";
    import { socket, type SocketMessage } from "@/store";

interface Message {
    fromPlayer: boolean;
    text: string;
}
let messageContainer: null | HTMLUnknownElement = null;
let input: null | HTMLElement = null;

let messages: Message[] = [];

let newMessageText = "";

let messageSubmitted = false;
let awaitingResponse = false;

let hasReceivedIndicator = false;

const send = async () => {
    if (newMessageText.length === 0 || awaitingResponse) return;

    messages.push({
        fromPlayer: true,
        text: newMessageText.trim(),
    });
    messages = messages;

    messageSubmitted = true;
    newMessageText = "";

    input?.blur();


    $socket!.send(JSON.stringify({
        content: newMessageText,
    }));
    

    awaitingResponse = true;

    hasReceivedIndicator = true;
    const receivedTimeout = setTimeout(() => hasReceivedIndicator = false, 2000);


    const newText: string = await new Promise(resolve => {
        const handleMessage = (event: MessageEvent) => {
            const data: SocketMessage<"msg"> = JSON.parse(event.data);

            switch (data.action) {
                case "msg":
                    resolve(data.payload.content);
                    break;

                default:
                    $socket!.addEventListener("message", handleMessage, {once: true});
                    break;
            }
        }

        $socket!.addEventListener("message", handleMessage, {once: true});
    });

    hasReceivedIndicator = false;
    clearTimeout(receivedTimeout);
    

    messages.push({
        fromPlayer: false,
        text: newText,
    });
    messages = messages;

    messageSubmitted = false;
    awaitingResponse = false;

    input?.focus();
};

$: messages, awaitingResponse, messageSubmitted, (async () => {
    await tick();
    messageContainer?.scrollTo(0, messageContainer.scrollHeight);
})();

const onkeydown = (event: KeyboardEvent) => {
    if (event.key === "Enter") {
        send();
        event.preventDefault();
    }
};



let nSecondsRemaining = 0;
let timerAnimationHandle = 0;
let timerAnimating = false;
const startTime = Date.now();
onMount(() => {
    const onNewFrame = (now: number) => {
        nSecondsRemaining = Math.max(0, 180 - Math.floor((Date.now() - startTime) / 1000));
        timerAnimationHandle = requestAnimationFrame(onNewFrame);
    };

    timerAnimationHandle = requestAnimationFrame(onNewFrame);
    timerAnimating = true;
});
onDestroy(() => {
    clearInterval(timerAnimationHandle);
});
</script>

<div class="chat-page">
    <top-bar>
        <ai-name-tag>
            Emily
        </ai-name-tag>

        <timer- class="strong-label">
            <!-- svelte-ignore a11y-missing-attribute -->
            <img src={timerStar}
                    class="timer-star"
                    class:animating={timerAnimating} />
            <span>{nSecondsRemaining}</span>
        </timer->
    </top-bar>
    
    <message-container bind:this={messageContainer}>
        <!-- <div class="spacer"></div> -->

        {#if messages.length > 0}
            {#each messages as message, index}
                <MessageBubble {...message}
                        hasSendingIndicator={index === messages.length - 1 && messageSubmitted && !awaitingResponse}
                        hasReceivedIndicator={index === messages.length - 1 && hasReceivedIndicator} />
            {/each}

            {#if awaitingResponse}
                <MessageBubble text=""
                        fromPlayer={false}
                        awaiting={true} />
            {/if}
        {:else}
            <div class="empty-message">Say something! The clock is ticking!</div>
        {/if}
    </message-container>

    <messenger->
        <div contenteditable
                bind:innerText={newMessageText}
                bind:this={input}
                on:keydown={onkeydown}
                class:disabled={messageSubmitted} />
    
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
    padding-bottom: 2rem;
}

top-bar {
    display: flex;
    align-items: center;
    justify-content: space-around;
    margin-top: -1.5rem;
    margin-left: -1rem;
    margin-right: -1rem;
}

ai-name-tag {
    background: linear-gradient(90deg, var(--col-red), #E94580);
    padding: 0.5rem;
    border: 0.6rem solid var(--col-yellow-light);
    width: 70%;
    font-weight: 700;
    transform: skewY(4deg) skewX(4deg);
}

timer- {
    font-size: 2rem;

    border-radius: 50%;
    aspect-ratio: 1;
    padding: 0.5rem;

    display: grid;
    place-items: center;

    > .timer-star {
        width: 6rem;
    }

    > img.animating {
        animation: rotate 1s infinite cubic-bezier(.14,.54,.22,1.06);

        @keyframes rotate {
            0% {
                transform: rotate(10deg);
            }

            100% {
                transform: rotate(130deg);
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
    // justify-content: flex-end;

    padding-top: 3rem;
    mask-image: linear-gradient(0deg, #000 90%, #0000);

    scroll-behavior: smooth;

    > .empty-message {
        opacity: 0.5;
    }
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

    &.disabled {
        pointer-events: none;
        opacity: 0.5;
    }
}
</style>