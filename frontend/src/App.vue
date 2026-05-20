<template>
  <div :class="['app-shell', { 'app-shell--login': isLoginRoute }]">
    <AppHeader v-if="!isLoginRoute" />
    <main class="app-content">
      <RouterView />
    </main>
  </div>
</template>

<script setup>
import { computed } from "vue";
import { RouterView } from "vue-router";
import { useRoute } from "vue-router";
import AppHeader from "./components/AppHeader.vue";

const route = useRoute();
const isLoginRoute = computed(() => route.name === "login");
</script>
