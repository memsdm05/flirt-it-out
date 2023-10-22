<script lang="ts">
import heart from "$/images/heart.svg";

let name = "";
</script>

<div>
    <img src={heart} alt="Heart" />

    <label class="strong-label"
            for="name-input">My name is</label>
    
    <form action="/register" method="post">
        <input type="text"
                bind:value={name}
                placeholder="your name"
                name="name"
                id="name-input"
                maxlength="12"
                tabindex="0" />

        <input type="submit"
                value="Register"
                disabled={name.length === 0} />
    </form>
</div>

<style lang="scss">
div {
    display: flex;
    flex-flow: column;
    align-items: flex-start;

    gap: 1rem;

    > form {
        display: flex;
        flex-flow: column;

        gap: 1rem;

        > input[type="submit"] {
            align-self: flex-end;
        }
    }


    > * {
        padding: 0 1.5rem;
    }
}

label {
    font-size: 2rem;
}
</style>