<template>
  <header class="header">
    <div class="header-inner glass-panel">
      <div>
        <p class="header-kicker">Video Project</p>
        <h1 class="header-title">视频平台控制台</h1>
      </div>
      <nav class="header-nav">
        <RouterLink to="/">登录</RouterLink>
        <RouterLink to="/workspace">工作台</RouterLink>
      </nav>
    </div>
  </header>
</template>

<script setup>
import { RouterLink } from "vue-router";
</script>

<style scoped>
.header {
  padding-top: 20px;
  color: #0f172a;
}

.header-inner {
  max-width: 1120px;
  margin: 0 auto;
  padding: 18px 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
}

.header-kicker {
  margin: 0 0 4px;
  font-size: 13px;
  color: rgba(71, 85, 105, 0.76);
}

.header-title {
  margin: 0;
  font-size: 22px;
}

.header-nav {
  display: flex;
  gap: 16px;
  color: rgba(30, 41, 59, 0.84);
}

.header-nav a.router-link-active {
  color: #0f172a;
  font-weight: 600;
}

@media (max-width: 720px) {
  .header-inner {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>
