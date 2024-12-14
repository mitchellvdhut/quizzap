<template>
  <div class="quizTile">
    <div class="newQuestionTile__header">
      <p>Vraag:</p>
      <div class="header_right">
        Tijd:
        <input class="time_input" type="number" v-model="question.answeringTimeInSeconds">
        <button class="remove_button" @click="() => onRemove(index)"><span><img src="/icons/trash_24px.png" alt="trash"></span></button>
      </div>
    </div>
    <input type="text" v-model="question.question" placeholder="Vul hier je vraag in" />
    <p>Antwoorden:</p>
    <div class="answers-list">
      <div class="answer" v-for="(answer, j) in question.answers" >
        <input type="checkbox" v-model="correctAnswers" :value="j">
        <input class="answer-field" v-model="question.answers[j].text" :placeholder="`Antwoord ${j + 1}`" />
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import type {Question} from "@/types";
import {ref} from "vue";

const props = defineProps<{
  index: number;
  question: Question
  onRemove: (index: number) => void
}>()

const correctAnswers = ref<number[]>(props.question.answers.map((answer, index) => answer.correct ? index : -1).filter(index => index !== -1));
</script>

<style lang="scss" scoped>
.quizTile {
  width: 100%;
  min-height: 150px;
  background-color: #29296c;
  border-radius: 15px;
  display: flex;
  flex-direction: column;
  padding: 1.5rem;
  color: white;
  gap: 1rem;

  .answer-field {
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
  input[type=checkbox] {
    width: 40px;
    height: 40px;
    border-radius: 5px;
  }

  .newQuestionTile__header {
    display: flex;
    justify-content: space-between;
  }
  input[type=text] {
    height: 40px;
    border-radius: 5px;
    padding: 0 0.5rem;
  }

  .header_right {
    display: flex;
    gap: 1rem;
    align-items: center;
    justify-content: center;
  }

  .time_input {
    width: 40px;
    height: 40px;
    text-align: center;
  }

  .remove_button {
     background-color: white;
     border-radius: 5px;
     width: 48px;
     height: 48px;
     border: none;
     cursor: pointer;
     user-select: none;

    img {
      width: 24px;
      height: 24px;
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
.answer {
  display: flex;
  flex-direction: row;
  gap: 1rem;
  flex-grow: 1;
  width: 100%;
}

@for $i from 1 through 4 {
  .answer:nth-child(3n + #{$i}) {
    .answer-field {
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
