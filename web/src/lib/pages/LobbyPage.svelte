<script lang="ts">
import { onDestroy, onMount } from "svelte";
import { botName, roundEnd, GameState, gameState, socket, type SocketMessage, type SocketMessageAction } from "@/store";

let displayedText = "The game will start shortly…";


const handleSocketMessage = (event: MessageEvent) => {
    const data: SocketMessage = JSON.parse(event.data);

    switch (data.action) {
        case "stasis":
            displayedText = (data as SocketMessage<"stasis">).payload.display;
            break;

        case "start_round": {
            const payload = (data as SocketMessage<"start_round">).payload;
            $botName = payload.bot_name;
            $roundEnd = new Date(payload.ends_at);

            $gameState = GameState.Chat;
            break;
        }
    }
}

onMount(() => {
    $socket!.addEventListener("message", handleSocketMessage);
});

onDestroy(() => {
    $socket?.removeEventListener("message", handleSocketMessage);
})
</script>

<div>
    <div>{displayedText}</div>
    <div class="dot"></div>
</div>

<style lang="scss">
.dot {
    width: 1.5rem;
    aspect-ratio: 1;
    margin-top: 1em;

    background: #fff;
    // border-radius: 50%;

    animation: throbber 1.25s infinite;
    @keyframes throbber {
        0% {
            transform: translateX(-48px);
        }

        0.1% {
            transform: translateX(0) scale(4, 0.25);
        }

        12.5% {
            transform: translateX(56px) scale(0.5, 2);
        }

        25% {
            transform: translateX(53px) scale(0.95, 1.1);
        }

        50% {
            transform: translateX(48px);
        }

        50.1% {
            transform: translateX(0) scale(4, 0.25);
        }

        62.5% {
            transform: translateX(-56px) scale(0.5, 2);
        }

        75% {
            transform: translateX(-53px) scale(0.95, 1.1);
        }

        100% {
            transform: translateX(-48px);
        }
    }
}
</style>