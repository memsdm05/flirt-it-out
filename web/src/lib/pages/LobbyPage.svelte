<script lang="ts">
import { onDestroy, onMount } from "svelte";
import { socket, type SocketMessage } from "@/store";

let displayedText = "The game will start shortly…";


const handleMessage = (event: MessageEvent) => {
    const data: SocketMessage<"stasis"> = JSON.parse(event.data);

    switch (data.action) {
        case "stasis":
            displayedText = data.payload.display;
            break;
    }
}

onMount(() => {
    $socket!.addEventListener("message", handleMessage);
});

onDestroy(() => {
    $socket?.removeEventListener("message", handleMessage);
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