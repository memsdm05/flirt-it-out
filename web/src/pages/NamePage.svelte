<script lang="ts">
import {username} from "@/store";

let name = "";
</script>

<name-page>
    <label>My name is</label>
    
    <input type="text"
            bind:value={name} />

    <button on:click={() => $username = name}>Next</button>
</name-page>

<style lang="scss">
name-page {
    display: flex;
    flex-flow: column;
    align-items: flex-start;

    > * {
        padding: 0 1.5rem;
    }
}

label {
    font-size: 2rem;
}
</style>