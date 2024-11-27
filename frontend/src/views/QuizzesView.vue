<template>
  <div class="quizzes-view">
    <div class="quizTile" v-for="quizze in quizzes" :key="quizze.id">
      <div class="quizTile__header">
        <p>{{quizze.name}}</p>
        <div class="header_right">
          <button class="remove_button" @click="() => onRemove(1)"><span><img src="/icons/trash_24px.png" alt="trash"></span></button>
        </div>
      </div>
    </div>
    <button class="add-quiz-button" @click="addQuiz">+ Nieuwe vraag toevoegen</button>
  </div>
</template>

<script lang="ts" setup>

import {ref} from "vue";
import NewQuestionTile from "@/components/NewQuestionTile.vue";

const quizzes = ref([{id: 1, name: "quiz 1"}])

function onRemove(index: number) {
  console.log('remove index', index)
}

function addQuiz() {
  console.log('add quiz')
}
</script>

<style lang="scss" scoped>
.quizzes-view {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 100%;
  max-width: 1280px;
  height: 100%;
  gap: 1rem;
}

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
}

.quizTile__header {
  display: flex;
  justify-content: space-between;
  font-size: 2rem;
}

.header_right {
  display: flex;
  gap: 1rem;
  align-items: center;
  justify-content: center;
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

.add-quiz-button {
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
