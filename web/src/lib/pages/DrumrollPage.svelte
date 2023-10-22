<div class="drumroll-page">
    <div class="strong-label">
        Rizz master?!?!
    </div>

    <div class="circle"></div>
</div>

<style lang="scss">
.drumroll-page {
    display: grid;
    place-items: center;

    > * {
        grid-area: 1/1;
    }
}

.circle {
    width: 8rem;
    aspect-ratio: 1;
    border: 2rem solid;
    border-color: #ffffff7f #ffffff7f #0000 #0000;
    border-radius: 50%;

    animation: rotate-uniform 1s infinite linear;

    @keyframes rotate-uniform {
        0% {
            transform: rotate(0turn);
        }
        100% {
            transform: rotate(1turn);
        }
    }
}
</style>