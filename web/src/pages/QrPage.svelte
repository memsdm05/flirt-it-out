<script lang="ts">
import {gameId} from "@/store";

</script>

<qr-page>
    <div>Scan the QR code on the board!</div>

    <button on:click={() => $gameId = "abc"}>Scan</button>
</qr-page>

<style lang="scss">
qr-page {
    display: flex;
    flex-flow: column;
    gap: 2.5rem;
}
</style>