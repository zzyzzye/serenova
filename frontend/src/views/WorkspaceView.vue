<template>
  <div class="workspace-view">
    <section class="glass-panel workspace-hero">
      <div>
        <p class="workspace-kicker">已登录</p>
        <h2>工作台入口</h2>
        <p>
          当前登录信息已经写入本地存储。后续可以在这里继续接用户中心、视频业务页、权限菜单和刷新令牌续期逻辑。
        </p>
      </div>
      <button class="ghost-button" type="button" @click="handleLogout">
        退出登录
      </button>
    </section>

    <section class="workspace-grid">
      <article class="glass-panel workspace-card">
        <span class="workspace-label">当前用户</span>
        <strong>{{ currentUser?.nickname || "未命名用户" }}</strong>
        <p>{{ currentUser?.username || "-" }}</p>
      </article>
      <article class="glass-panel workspace-card">
        <span class="workspace-label">接口状态</span>
        <strong>{{ loading ? "读取中" : "已连接" }}</strong>
        <p>{{ errorMessage || "登录响应已完成，可继续接入 /auth/me。" }}</p>
      </article>
    </section>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from "vue";
import { useRouter } from "vue-router";

import { fetchCurrentUser, getStoredAuthState, logout } from "../services/auth";

const router = useRouter();
const authState = ref(getStoredAuthState());
const loading = ref(false);
const errorMessage = ref("");

const currentUser = computed(() => authState.value?.user || null);

async function handleLogout() {
  await logout();
  router.push({ name: "login" });
}

onMounted(async () => {
  if (!authState.value?.accessToken) {
    errorMessage.value = "尚未检测到本地登录态，已返回登录页更合适。";
    router.replace({ name: "login" });
    return;
  }

  loading.value = true;
  try {
    const user = await fetchCurrentUser();
    authState.value = {
      ...authState.value,
      user,
    };
  } catch (error) {
    errorMessage.value = error?.response?.data?.detail || "当前登录态校验失败，请重新登录。";
  } finally {
    loading.value = false;
  }
});
</script>

<style scoped>
.workspace-view {
  display: grid;
  gap: 24px;
}

.workspace-hero {
  min-height: 220px;
  padding: 28px;
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 24px;
}

.workspace-kicker,
.workspace-label {
  margin: 0 0 10px;
  font-size: 13px;
  color: rgba(71, 85, 105, 0.78);
}

.workspace-hero h2 {
  margin: 0;
  font-size: 32px;
}

.workspace-hero p {
  max-width: 640px;
  margin: 12px 0 0;
  color: rgba(51, 65, 85, 0.84);
}

.workspace-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 20px;
}

.workspace-card {
  min-height: 180px;
  padding: 24px;
}

.workspace-card strong {
  display: block;
  font-size: 22px;
}

.workspace-card p {
  margin: 12px 0 0;
  color: rgba(51, 65, 85, 0.84);
}

@media (max-width: 900px) {
  .workspace-hero {
    align-items: flex-start;
    flex-direction: column;
  }

  .workspace-grid {
    grid-template-columns: 1fr;
  }
}
</style>
