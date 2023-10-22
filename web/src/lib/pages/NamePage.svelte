<script lang="ts">
import { goto } from "$app/navigation";
import {username} from "@/store";

let name = "";

const onSubmitName = () => {
    if (name.length === 0) return;

    $username = name;
    goto("/");
};
</script>

<div>
    <label class="strong-label"
            for="name-input">My name is</label>
    
    <input type="text"
            bind:value={name}
            placeholder="your name"
            id="name-input" />

    <div>
        <button on:click={onSubmitName}
                disabled={name.length === 0}>Next</button>
    </div>
</div>

<style lang="scss">
div {
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