<script lang="ts">
// import {gameId} from "@/store";

</script>

<div class="qr-page">
    <div>Scan the QR code on the board!</div>

    <a href="/register/">
        <button on:click={() => {/* $gameId = "abc" */}}>
            Scan
        </button>
    </a>
</div>

<style lang="scss">
.qr-page {
    display: flex;
    flex-flow: column;
    gap: 2.5rem;
}
</style>