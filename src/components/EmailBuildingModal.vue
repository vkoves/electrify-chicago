<template>
  <Popup class="email-this-building" @close="close()">
    <div class="header">
      <img src="/email.svg" alt="" />
      <h1 autofocus>Email This Building</h1>
    </div>

    <div class="email-prompt-wrapper">
      <h1 class="prompt">Do you know this building's owner?</h1>
      <p class="description">
        Send them an email asking about their electrification plan!
      </p>
      <div class="email-this-building-subheader">
        <h2>Subject</h2>

        <button class="copy-btn" @click="copySubject">
          Copy Subject
          <img src="/copy.svg" alt="" />
        </button>

        <!-- Will say 'Copied' after copying -->
        <div ref="subj-copied" aria-live="polite" class="copy-notice" />
      </div>
      <p ref="email-subj" class="email-box">
        What Is Our Building's Plan For Saving Energy & Reducing Emissions?
      </p>
      <div class="email-this-building-subheader">
        <h2>Body</h2>

        <button class="copy-btn" @click="copyBody">
          Copy Body
          <img src="/copy.svg" alt="" />
        </button>

        <!-- Will say 'Copied' after copying -->
        <div ref="body-copied" aria-live="polite" class="copy-notice" />
      </div>
      <div ref="email-body" class="email-box -body">
        <p>Dear sir or madam,</p>
        <p>
          My name is <span class="to-replace">_NAME_</span>, and I am an
          <span class="to-replace">_OWNER/OCCUPANT/OTHER_</span> of
          {{ building.PropertyName }}.
        </p>
        <p>
          I've been reading about {{ building.PropertyName }}'s emissions and
          energy use, and I wanted to learn more about your plans to improve our
          energy efficiency, electrify the building, and reduce our emissions.
          Well insulated all-electric buildings have lower energy bills, cleaner
          air, and are more comfortable for their occupants, and I want to make
          sure there is a concrete plan to make {{ building.PropertyName }} one
          of those buildings!
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
  readonly CopyNoticeDurMs: number = 1500;

  @Prop({ required: true }) building!: IBuilding;

  /** Emit on modal close */
  @Emit()
  close(): boolean {
    return true;
  }

  copyElementTextToClipboard(
    contentRef: HTMLElement,
    noticeRef: HTMLElement,
  ): void {
    try {
      const content = contentRef.innerText;
      navigator.clipboard.writeText(content);
      this.showCopiedNotice(noticeRef);
    } catch (error) {
      console.error(error);
    }
  }

  /**
   * Fade in and out a copy notice
   */
  showCopiedNotice(noticeElem: HTMLElement): void {
    // Show a "Copied" message
    noticeElem.innerText = 'Copied!';
    noticeElem.classList.add('-visible');

    setTimeout(() => {
      noticeElem.classList.remove('-visible');

      // Wait till after the animation to remove the text
      setTimeout(() => (noticeElem.innerText = ''), 300);
    }, this.CopyNoticeDurMs);
  }

  copyBody(): void {
    this.copyElementTextToClipboard(
      this.$refs['email-body'] as HTMLElement,
      this.$refs['body-copied'] as HTMLElement,
    );
  }

  copySubject(): void {
    this.copyElementTextToClipboard(
      this.$refs['email-subj'] as HTMLElement,
      this.$refs['subj-copied'] as HTMLElement,
    );
  }
}
</script>

<style lang="scss">
dialog.email-this-building {
  .popup-inner {
    max-width: 37.5rem; // 600px
    margin: auto auto;
  }

  * {
    margin: 0;
    padding: 0;
  }

  .header {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 2rem;
    background-color: #0066ff;
    color: $white;
    padding: 1.5rem;

    img {
      height: 2rem;
    }
  }

  h2 {
    margin: 1rem 0 0;
  }

  .email-prompt-wrapper {
    padding: 2rem;

    .prompt {
      font-size: 1.75rem;
      font-weight: 700;
    }
  }

  .email-this-building-subheader {
    display: flex;
    gap: 0.5rem;
    margin-top: 0.75rem;
    margin-bottom: 0.2rem;
    align-items: flex-end;

    button.copy-btn {
      background-color: $blue-dark;
      color: $white;
      font-weight: bold;
      border: none;
      padding: 0.25rem 0.5rem;
      margin-left: 0.5rem;
      margin-bottom: 0.2rem;

      &:hover,
      &:focus {
        background-color: $blue-very-dark;
      }

      img {
        height: 0.75rem;
        margin-left: 0.4rem;
      }
    }
  }

  .copy-notice {
    margin-left: 0.25rem;
    margin-bottom: 0.4rem;
    opacity: 0;
    transition: opacity 0.3s; // fade in text

    &.-visible {
      opacity: 1;
    }
  }

  .email-box {
    border: solid $border-thin $black;
    padding: 0.75rem;
    border-radius: $brd-rad-small;

    &.-body {
      padding: 1rem 0.75rem;
    }

    p + p {
      margin-top: 1em;
    }

    .to-replace {
      font-weight: 700;
      font-style: italic;
    }
  }

  /** Mobile Styling */
  @media (max-width: $mobile-max-width) {
    h1 {
      font-size: 1.5rem;
    }
  }
}
</style>
