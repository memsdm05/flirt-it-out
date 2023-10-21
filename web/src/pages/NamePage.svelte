<script lang="ts">
import {username} from "@/store";

let name = "";
</script>

<name-page>
    <label class="strong-label"
            for="name-input">My name is</label>
    
    <input type="text"
            bind:value={name}
            placeholder="your name"
            id="name-input" />

    <div>
        <button on:click={() => $username = name}>Next</button>
    </div>
</name-page>

<style lang="scss">
name-page {
    display: flex;
    flex-flow: column;
    align-items: flex-start;

    gap: 1rem;

    > * {
        padding: 0 1.5rem;
    }

    > div {
        align-self: flex-end;
    }
}

label {
    font-size: 2rem;
}
</style>