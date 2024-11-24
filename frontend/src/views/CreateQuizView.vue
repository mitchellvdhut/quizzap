<template>
  <div class="create">
    <h1>create quiz view</h1>
    <NewQuestionTile
      v-for="(question, index) in questions"
      :index="index"
      :question="question"
      :on-remove="removeQuestion"
    />
    <button class="add-question-button" @click="addQuestion">+ Nieuwe vraag toevoegen</button>
  </div>
</template>

<script setup lang="ts">
import {ref} from "vue";
import NewQuestionTile from "@/components/NewQuestionTile.vue";
import type {Question} from "@/types";

const questions = ref<Question[]>(
  [
    {
      question: "",
      answers: [
        {
          text: "",
          correct: false,
        },
        {
          text: "",
          correct: false,
        },
        {
          text: "",
          correct: false,
        },
        {
          text: "",
          correct: true,
        }
      ],
      answeringTimeInSeconds: 20
    }
  ]
)

function addQuestion() {
  const question: Question = {
    question: "",
      answers: [
    {
      text: "",
      correct: true,
    },
    {
      text: "",
      correct: false,
    },
    {
      text: "",
      correct: false,
    },
    {
      text: "",
      correct: false,
    }
  ],
    answeringTimeInSeconds: 20
  }
  questions.value.push(question)
}

function removeQuestion(index: number) {
  questions.value.splice(index, 1);
}

</script>

<style lang="scss" scoped>
.create {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 100%;
  max-width: 1280px;
  height: 100%;
  gap: 1rem;
}


.add-question-button {
  width: 100%;
  height: 48px;
  border-radius: 15px;
  border: none;
  font-size: 1.5rem;
  transition: all .05s linear 0s;
  top: 0;
  left: 0;
  position: relative;

  $button-color: #63d1bb;;
  $button-shadow-color: color.adjust($button-color, $lightness: -15%);
  background-color: $button-color;
  box-shadow: -6px 6px 0 $button-shadow-color;

  &:hover {
    top: 3px;
    left: -3px;
    box-shadow: -3px 3px 0 $button-shadow-color;
  }
  &:active {
    top: 6px;
    left: -6px;
    box-shadow: none;
  }
}
</style>
