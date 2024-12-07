<template>
  <Popup
    class="email-this-building"
    @close="close()"
  >
    <div class="header">
      <img
        src="/email.svg"
        alt=""
      >
      <h1 autofocus>
        Email This Building
      </h1>
    </div>

    <div class="email-prompt-wrapper">
      <h1 class="prompt">
        Do you know this building's owner?
      </h1>
      <p class="description">
        Send them an email asking about their electrification plan!
      </p>
      <div class="email-this-building-subheader">
        <h2>Subject</h2>

        <button
          class="copy-btn"
          @click="copySubject"
        >
          Copy Subject
          <img
            src="/copy.svg"
            alt=""
          >
        </button>

        <!-- Will say 'Copied' after copying -->
        <div
          ref="subj-copied"
          aria-live="polite"
          class="copy-notice"
        />
      </div>
      <p
        id="email-subj"
        class="email-box"
      >
        What's Our Building's Plan For Reducing Emissions?
      </p>
      <div class="email-this-building-subheader">
        <h2>Body</h2>

        <button
          class="copy-btn"
          @click="copyBody"
        >
          Copy Body
          <img
            src="/copy.svg"
            alt=""
          >
        </button>

        <!-- Will say 'Copied' after copying -->
        <div
          ref="body-copied"
          aria-live="polite"
          class="copy-notice"
        />
      </div>
      <div
        id="email-body"
        class="email-box -body"
      >
        <p>
          Dear sir or madam,
        </p>
        <p>
          My name is <span class="to-replace">_NAME_</span>, and I am an
          <span class="to-replace">_OWNER/OCCUPANT/OTHER_</span> of
          {{ building.PropertyName }}.
        </p>
        <p>
          I've been reading about {{ building.PropertyName }}'s emissions and energy use,
          and I wanted to learn more about your plans to improve our energy efficiency,
          electrify the building, and reduce our emissions. Well insulated all-electric
          buildings have lower energy bills, cleaner air, and are more comfortable for their
          occupants, and I want to make sure there is a concrete plan to make
          {{ building.PropertyName }} one of those buildings!
        </p>
        <p>
          You can see more at
          <strong>https://electrifychicago.net{{ building.path }}</strong>
        </p>
      </div>
    </div>
  </Popup>
</template>

<script lang="ts">
import { Component, Emit, Prop, Vue } from 'vue-property-decorator';
import { IBuilding } from '../common-functions.vue';
import Popup from '../components/layout/Popup.vue';

/**
 * A modal to email a given building
 */
 @Component({
    components: {
        Popup,
    },
 })
export default class EmailBuildingModal extends Vue {
  @Prop({required: true}) building!: IBuilding;

  /** Emit on modal close */
  @Emit()
  close(): boolean {
    return true;
  }

  copyElementTextToClipboard(id: string, noticeRef: HTMLElement): void {
    try {
      const content = document.getElementById(id)!.innerText;
      navigator.clipboard.writeText(content);

      // Show a "Copied" message
      noticeRef.innerText = 'Copied!';
      noticeRef.classList.add('-visible');

      setTimeout(() => {
        noticeRef.classList.remove('-visible');

        // Wait till after the animation to remove the text
        setTimeout(() => noticeRef.innerText = '', 300);
      }, 1500);
    }
    catch (error) {
      console.error(error);
    }
  }

  copyBody(): void {
    this.copyElementTextToClipboard('email-body', this.$refs['body-copied'] as HTMLElement);
  }

  copySubject(): void {
    this.copyElementTextToClipboard('email-subj', this.$refs['subj-copied'] as HTMLElement);
  }
}
</script>

<style lang="scss">
.new-tab-icon {
  width: 1em;
  height: 1em;
}
</style>
