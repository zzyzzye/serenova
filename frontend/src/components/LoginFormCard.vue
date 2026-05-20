<template>
  <section class="glass-panel login-card">
    <div class="card-glow" aria-hidden="true" />
    <div class="login-card-top">
      <div>
        <p class="login-card-kicker">账号登录</p>
        <h3>进入控制台</h3>
      </div>
      <div class="card-status">
        <div class="signal-dot" />
        <span>online</span>
      </div>
    </div>

    <div class="login-card-copy">
      <p>使用管理员账号进入控制台，登录后会立即校验当前令牌并同步用户信息。</p>
    </div>

    <form class="login-form" @submit.prevent="handleSubmit">
      <label class="field">
        <span>用户名</span>
        <input
          v-model.trim="form.username"
          type="text"
          name="username"
          autocomplete="username"
          placeholder="请输入用户名"
        />
      </label>

      <label class="field">
        <span>密码</span>
        <input
          v-model="form.password"
          type="password"
          name="password"
          autocomplete="current-password"
          placeholder="请输入密码"
        />
      </label>

      <div class="hint-row">
        <span>演示账号：admin</span>
        <span>演示密码：admin123456</span>
      </div>

      <p v-if="errorMessage" class="feedback error-text">{{ errorMessage }}</p>
      <p v-else-if="successMessage" class="feedback success-text">{{ successMessage }}</p>

      <button class="primary-button" type="submit" :disabled="submitting">
        {{ submitting ? "登录中..." : "登录" }}
      </button>
    </form>
  </section>
</template>

<script setup>
import { reactive, ref } from "vue";

import { login } from "../services/auth";

const emit = defineEmits(["login-success"]);

const form = reactive({
  username: "admin",
  password: "admin123456",
});
const submitting = ref(false);
const errorMessage = ref("");
const successMessage = ref("");

async function handleSubmit() {
  if (!form.username || !form.password) {
    errorMessage.value = "请输入用户名和密码。";
    successMessage.value = "";
    return;
  }

  submitting.value = true;
  errorMessage.value = "";
  successMessage.value = "";

  try {
    await login({
      username: form.username,
      password: form.password,
    });
    successMessage.value = "登录成功，正在进入工作台。";
    emit("login-success");
  } catch (error) {
    errorMessage.value =
      error?.response?.data?.detail || "登录失败，请确认后端服务与账号信息。";
  } finally {
    submitting.value = false;
  }
}
</script>

<style scoped>
.login-card {
  overflow: hidden;
  padding: 28px 28px 30px;
}

.card-glow {
  position: absolute;
  inset: auto;
  right: -36px;
  top: -44px;
  width: 160px;
  height: 160px;
  border-radius: 999px;
  background: radial-gradient(circle at 34% 34%, rgba(255, 255, 255, 0.92), rgba(96, 165, 250, 0.24) 44%, transparent 70%);
  filter: blur(6px);
  pointer-events: none;
}

.login-card-top {
  position: relative;
  z-index: 1;
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 16px;
}

.login-card-kicker {
  margin: 0 0 8px;
  font-size: 13px;
  color: rgba(71, 85, 105, 0.7);
}

.login-card h3 {
  margin: 0;
  font-size: 42px;
  line-height: 1;
}

.card-status {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 8px 12px;
  border-radius: 999px;
  color: rgba(30, 64, 175, 0.82);
  background: rgba(255, 255, 255, 0.34);
  border: 1px solid rgba(255, 255, 255, 0.48);
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.72);
}

.card-status span {
  font-size: 12px;
  text-transform: uppercase;
}

.signal-dot {
  width: 14px;
  height: 14px;
  border-radius: 999px;
  background: radial-gradient(circle at 30% 30%, #ffffff 0%, #93c5fd 38%, #2563eb 100%);
  box-shadow: 0 0 24px rgba(59, 130, 246, 0.42);
}

.login-card-copy {
  position: relative;
  z-index: 1;
  margin-top: 20px;
}

.login-card-copy p {
  margin: 0;
  max-width: 420px;
  color: rgba(51, 65, 85, 0.76);
  line-height: 1.65;
}

.login-form {
  position: relative;
  z-index: 1;
  margin-top: 26px;
  display: grid;
  gap: 18px;
}

.field {
  display: grid;
  gap: 12px;
}

.field span {
  font-size: 13px;
  color: rgba(51, 65, 85, 0.74);
  text-transform: uppercase;
}

.field input {
  width: 100%;
  min-height: 60px;
  padding: 0 20px;
  font-size: 17px;
  color: #0f172a;
  background: linear-gradient(180deg, rgba(255, 255, 255, 0.58), rgba(255, 255, 255, 0.36));
  border: 1px solid rgba(255, 255, 255, 0.58);
  border-radius: 20px;
  box-shadow:
    inset 0 1px 0 rgba(255, 255, 255, 0.74),
    0 10px 22px rgba(148, 163, 184, 0.08);
  backdrop-filter: blur(18px);
  -webkit-backdrop-filter: blur(18px);
  outline: none;
  transition: border-color 160ms ease, box-shadow 160ms ease, background 160ms ease;
}

.field input:focus {
  border-color: rgba(59, 130, 246, 0.5);
  background: rgba(255, 255, 255, 0.68);
  box-shadow:
    0 0 0 4px rgba(96, 165, 250, 0.14),
    0 18px 30px rgba(96, 165, 250, 0.12);
}

.hint-row {
  display: flex;
  flex-wrap: wrap;
  gap: 10px 12px;
  color: rgba(71, 85, 105, 0.76);
  font-size: 13px;
}

.hint-row span {
  padding: 8px 12px;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.28);
  border: 1px solid rgba(255, 255, 255, 0.44);
}

.feedback {
  min-height: 22px;
  margin: 0;
  font-size: 14px;
}

.error-text {
  color: #b91c1c;
}

.success-text {
  color: #166534;
}

.primary-button {
  min-height: 62px;
  margin-top: 6px;
  font-size: 20px;
  font-weight: 600;
  border-radius: 20px;
}

@media (max-width: 640px) {
  .login-card {
    padding: 24px 20px;
  }

  .login-card h3 {
    font-size: 36px;
  }
}
</style>
