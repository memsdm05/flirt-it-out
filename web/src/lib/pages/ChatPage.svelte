<script lang="ts">
import { afterUpdate, onDestroy, onMount, tick } from "svelte";
import { fly } from "svelte/transition";
import { cubicOut } from "svelte/easing";
import MessageBubble from "$/MessageBubble.svelte";

import timerStar from "$/images/timer-star.svg";
import { botName, GameState, gameState, roundEnd, socket, type SocketMessage } from "@/store";


const CHAR_LIMIT = 140;

interface Message {
    fromPlayer: boolean;
    text: string;
}
let messageContainer: null | HTMLUnknownElement = null;
let input: null | HTMLElement = null;

let messages: Message[] = [];

let newMessageText = "";
$: charCount = newMessageText.trim().length;

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

    input?.blur();


    $socket!.send(JSON.stringify({
        action: "msg",
        payload: {
            content: newMessageText,
        }
    }));

    newMessageText = "";
    

    awaitingResponse = true;

    hasReceivedIndicator = true;
    const receivedTimeout = setTimeout(() => hasReceivedIndicator = false, 2000);


    const newText: string = await new Promise(resolve => {
        const handleMessage = (event: MessageEvent) => {
            const data: SocketMessage = JSON.parse(event.data);

            switch (data.action) {
                case "msg":
                    resolve((data as SocketMessage<"msg">).payload.content);
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

const onfocus = (event: FocusEvent) => {
    if (messageSubmitted) {
        input?.blur();
    }
};



let nSecondsRemaining = 0;
let timerAnimationHandle = 0;
let timerAnimating = false;
onMount(() => {
    const onNewFrame = (now: number) => {
        if (Date.now() > $roundEnd.getTime()) {
            $gameState = GameState.Scoring;
            return;
        }

        nSecondsRemaining = Math.max(0, Math.floor(($roundEnd.getTime() - Date.now()) / 1000));
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
            {$botName}
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
                on:keypress={event => charCount > CHAR_LIMIT && event.preventDefault()}
                on:focus={onfocus}
                class:disabled={messageSubmitted} />
    
        <div class="messenger-bottom-row">
            {charCount} / {CHAR_LIMIT}
            <button on:click={send}
                    disabled={!messageSubmitted && newMessageText.trim().length === 0}>Send</button>
        </div>
        
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

    > .messenger-bottom-row {
        display: flex;
        gap: 1rem;
        justify-content: space-around;
        align-items: center;
    }
}

[contenteditable] {
    word-break: break-word;

    padding-left: 0.5em;
    padding-right: 0.5em;

    text-align: left;

    &.disabled {
        pointer-events: none;
        opacity: 0.5;
    }
}
</style>