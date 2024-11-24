<template>
  <div class="question-view">
    <BaseTile v-for="answer in answers" :answer="answer" class="answer"/>
  </div>
</template>

<script lang="ts" setup>
import BaseTile from "@/components/BaseTile.vue";
import {ref} from "vue";

const answers = ref(["antwoord 1", "antwoord 2", "antwoord 3", "antwoord 4"] as const);
</script>

<style lang="scss" scoped>
.question-view {
  max-width: 1280px;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}
.answer {
  cursor: pointer;
  font-family: $font-family;
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

</style>
