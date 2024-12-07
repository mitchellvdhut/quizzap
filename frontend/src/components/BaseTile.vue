<template>
  <div class="tile">
    {{ answer }}
  </div>
</template>

<script lang="ts" setup>

const props = defineProps({
  answer: String
})

</script>

<style lang="scss" scoped>
.tile {
  border-radius: 15px;
  width: 450px;
  height: 150px;
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
}
</style>
