<template>
  <div class="question-view">
    <QuestionText :question="question"/>
    <div class="answer-section">
    <BaseTile v-for="answer in answers" :answer="answer" class="answer"/>
    </div>
  </div>
</template>

<script lang="ts" setup>
import BaseTile from "@/components/BaseTile.vue";
import QuestionText from "@/components/QuestionText.vue";
import {ref} from "vue";

const question = ref("Wat is het antwoord op de vraag?")
const answers = ref(["antwoord 1", "antwoord 2", "antwoord 3", "antwoord 4"] as const);
</script>

<style lang="scss" scoped>
.question-view {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
  gap: 6rem;
}
.answer-section {
  max-width: 1280px;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}
.answer {
  cursor: pointer;
  font-weight: 700;
  font-size: 2rem;
}

@for $i from 1 through 4 {
  .answer {
    transition: all .05s linear 0s;
    top: 0;
    left: 0;
    &:nth-child(3n + #{$i}) {
      $tile-color: map.get($tile-colors, $i);
      $tile-shadow-color: color.adjust($tile-color, $lightness: -15%);
      $tile-text-color: color.adjust($tile-color, $lightness: 30%);
      background-color: $tile-color;
      color: $tile-text-color;
      box-shadow: -6px 6px 0 $tile-shadow-color;
      position: relative;
      user-select: none;

      &:hover {
        top: 3px;
        left: -3px;
        box-shadow: -3px 3px 0 $tile-shadow-color;
      }
      &:active {
        top: 6px;
        left: -6px;
        box-shadow: none;
      }
    }
  }
}

@media only screen and (max-width: 948px) {
  .answer-section {
    width: calc(100% - 2rem);
    padding-inline: 1rem;
    grid-template-columns: 1fr;
  }
  .answer {
    width: 100%;
  }
}

</style>
