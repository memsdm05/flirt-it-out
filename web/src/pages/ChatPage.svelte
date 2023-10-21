<script lang="ts">
import MessageBubble from "$/MessageBubble.svelte";


interface Message {
    fromPlayer: boolean;
    text: string;
}
let messages: Message[] = [
    {fromPlayer: false, text: "hello"},
    {fromPlayer: true, text: "hello"},
    {fromPlayer: false, text: "hello"},
    {fromPlayer: true, text: "hello"},
];

let newMessageText = "";

const send = () => {
    messages.push({
        fromPlayer: true,
        text: newMessageText,
    });
    messages = messages;

    newMessageText = "";
};
</script>

<chat-page>
    <message-container>
        {#each messages as message}
            <MessageBubble {...message} />
        {/each}
    </message-container>

    <div contenteditable
            bind:innerText={newMessageText} />

    <button on:click={send}>Send</button>
</chat-page>

<style lang="scss">
chat-page {
    display: flex;
    flex-flow: column;
    justify-items: space-between;
    gap: 1rem;
}

message-container {
    display: flex;
    flex-flow: column;
    gap: 0.5rem;
}

[contenteditable] {
    word-break: break-word;

    padding-left: 0.5em;
    padding-right: 0.5em;
}
</style>