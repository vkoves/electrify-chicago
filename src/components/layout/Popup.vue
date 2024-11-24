<template>
    <div class="popup">
        <div class="popup-inner">
            <slot />
            <button class="popup-close">Close</button>
        </div>
    </div>
</template>

<script lang="ts">
export default {

}
</script>

<style lang="scss">
.popup {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    z-index: 99;
    background-color: rgba(0, 0, 0, 0.2);
    display: flex;
    align-items: center;
    justify-content: center;

    .popup-inner {
        background-color: #fff;
        display: flex;
        flex-direction: column;

        .popup-close {
            align-self: center;
            border: none;
            border-radius: 0.25rem;
            background-color: #eeeeee;
            padding: 0.25rem 1rem;
            margin-bottom: 1rem;
            font-size: 0.75rem;
            font-weight: 300;
        }
    }
}
</style>