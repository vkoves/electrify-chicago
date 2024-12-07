<template>
  <dialog id="dialog">
    <div class="popup-inner">
      <slot />
      <button
        class="popup-close"
        @click="close"
      >
        Close
      </button>
    </div>
  </dialog>
</template>

<script lang="ts">
import { Component, Vue, Emit } from 'vue-property-decorator';

@Component
export default class Popup extends Vue {
  dialog!: HTMLDialogElement;

  @Emit()
  close(): boolean {
    this.dialog.close();
    return true;
  }

  /** Open the dialog on load */
  mounted(): void {
    this.dialog = document.getElementById('dialog') as HTMLDialogElement;

    this.dialog.showModal();

    // The native <dialog> handles Esc to close, so we then emit
    this.dialog.addEventListener("close", () => {
      this.close();
    });
  }
}
</script>

<style lang="scss">
dialog {
  margin: auto;
  padding: 0;
  border: none;
  border-radius: $brd-rad-medium;

  &::backdrop {
    background-color: rgba(0, 0, 0, 0.4);
    backdrop-filter: blur(0.25rem);
  }

  .popup-inner {
    background-color: $white;
    display: flex;
    flex-direction: column;
    border-radius: 0.25rem;

    .popup-close {
      align-self: center;
      border: none;
      border-radius: 0.25rem;
      padding: 0.5rem 2rem;
      margin-bottom: 1rem;
      background-color: $grey-light;
      font-size: 1.25rem;

      &:hover, &:focus { background-color: $grey; }
    }
  }
}
</style>