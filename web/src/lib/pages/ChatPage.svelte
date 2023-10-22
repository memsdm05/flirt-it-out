<script lang="ts">
import MessageBubble from "$/MessageBubble.svelte";
    import { afterUpdate } from "svelte";


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

const send = () => {
    messages.push({
        fromPlayer: true,
        text: newMessageText,
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

<chat-page>
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
</chat-page>

<style lang="scss">
chat-page {
    display: flex;
    flex-flow: column;
    justify-content: space-between;
    gap: 1rem;
}

message-container {
    display: flex;
    flex-flow: column;
    gap: 0.5rem;

    overflow-y: auto;
    flex-grow: 1;
    flex-shrink: 1;
    height: 0; // sure thing buddy

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