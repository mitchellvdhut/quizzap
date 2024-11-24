<template>
  <div class="newQuestionTile">
    <div class="newQuestionTile__header">
      <p>Vraag:</p>
      <button class="remove_button" @click="() => onRemove(index)">DELETE</button>
    </div>
    <input v-model="question.question" placeholder="Vul hier je vraag in" />
    <p>Antwoorden:</p>
    <div class="answers-list">
      <input class="answer-field" v-for="(answer, j) in question.answers" v-model="question.answers[j].text" :placeholder="`Antwoord ${j}`" />
    </div>
  </div>
</template>

<script lang="ts" setup>
import type {Question} from "@/types";

const props = defineProps<{
  index: number;
  question: Question
  onRemove: (index: number) => void
}>()

</script>

<style lang="scss" scoped>
.newQuestionTile {
  width: 100%;
  min-height: 150px;
  background-color: #29296c;
  border-radius: 15px;
  display: flex;
  flex-direction: column;
  padding: 1.5rem;
  color: white;
  gap: 1rem;

  .newQuestionTile__header {
    display: flex;
    justify-content: space-between;

    .remove_button {
      background-color: white;
      border-radius: 5px;
      width: 48px;
      height: 48px;
      border: none;
      cursor: pointer;
      user-select: none;
    }
  }

  input {
    width: calc(100% - 0.5rem);
    height: 40px;
    box-sizing: border-box;
    padding: 0 0.5rem;
    border-radius: 5px;
    border: none;
    background-color: #1a1f37;
    color: white;

    &::placeholder {
      color: white;
      opacity: 1; /* Firefox */
    }

    &::-ms-input-placeholder { /* Edge 12 -18 */
      color: white;
    }
  }

}

.answers-list {
  width: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  flex-wrap: wrap;
  gap: 1rem;
}

@for $i from 1 through 4 {
  .answer-field {
    &:nth-child(3n + #{$i}) {
      $field-color: map.get($tile-colors, $i);
      $field-shadow-color: color.adjust($field-color, $lightness: -15%);
      $field-background-color: color.adjust($field-color, $lightness: 30%);
      border-radius: 5px;
      border: none;
      background-color: $field-background-color;
      box-shadow: -3px 3px 0 $field-shadow-color;
      position: relative;
      color: $field-shadow-color;
      width: calc(100% - 1rem);

      &::placeholder {
        color: $field-shadow-color;
        opacity: 1; /* Firefox */
      }

      &::-ms-input-placeholder { /* Edge 12 -18 */
        color: $field-shadow-color;
      }
    }
  }
}

</style>
