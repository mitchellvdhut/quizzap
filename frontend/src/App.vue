<script setup lang="ts">
import { RouterView } from 'vue-router'
import { startWebsocket } from './api/websocket';

const websocket = startWebsocket(`/quizCreate/kXG8?token=ANARCHY`)

websocket.onStatusCode = (packet) => {
  console.log("Result", packet);
}

websocket.onSessionCreated = (packet) => {
  console.log(`SessionID: ${packet.payload.session_id}`);
}

</script>

<template>
  <main>
    <RouterView />
  </main>
</template>

<style>
#app {
  width: 100%;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

main {
  width: 100%;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  box-sizing: border-box;
  color: white;
  padding: 5rem 1rem;
}
</style>
