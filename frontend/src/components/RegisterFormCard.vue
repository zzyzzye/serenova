<template>
  <section class="glass-panel register-card">
    <div class="register-card-top">
      <div>
        <p class="register-card-kicker">创建账号</p>
        <h3>注册</h3>
      </div>
    </div>

    <form class="register-form" @submit.prevent="handleSubmit">
      <label class="field">
        <span>用户名</span>
        <input
          v-model.trim="form.username"
          type="text"
          name="username"
          autocomplete="username"
          placeholder="3-64 个字符"
          @focus="$emit('input-focus')"
          @blur="$emit('input-blur')"
        />
      </label>

      <label class="field">
        <span>昵称</span>
        <input
          v-model.trim="form.nickname"
          type="text"
          name="nickname"
          autocomplete="nickname"
          placeholder="1-64 个字符"
          @focus="$emit('input-focus')"
          @blur="$emit('input-blur')"
        />
      </label>

      <label class="field">
        <span>邮箱</span>
        <input
          v-model.trim="form.email"
          type="email"
          name="email"
          autocomplete="email"
          placeholder="用于密码找回"
          @focus="$emit('input-focus')"
          @blur="$emit('input-blur')"
        />
      </label>

      <label class="field">
        <span>密码</span>
        <input
          v-model="form.password"
          type="password"
          name="new-password"
          autocomplete="new-password"
          placeholder="至少 6 个字符"
          @focus="$emit('input-focus')"
          @blur="$emit('input-blur')"
        />
      </label>

      <label class="field">
        <span>确认密码</span>
        <input
          v-model="form.confirmPassword"
          type="password"
          name="confirm-password"
          autocomplete="new-password"
          placeholder="再次输入密码"
          @focus="$emit('input-focus')"
          @blur="$emit('input-blur')"
        />
      </label>

      <p v-if="errorMessage" class="feedback error-text">{{ errorMessage }}</p>
      <p v-else-if="successMessage" class="feedback success-text">{{ successMessage }}</p>

      <button
        class="primary-button"
        type="submit"
        :disabled="submitting"
        @mouseenter="$emit('btn-enter')"
        @mouseleave="$emit('btn-leave')"
      >
        {{ submitting ? "注册中..." : "注册" }}
      </button>
    </form>

    <div class="card-switch-links">
      <a href="#" @click.prevent="$emit('switch-panel', 'login')">已有账号？登录</a>
    </div>
  </section>
</template>

<script setup>
import { reactive, ref } from "vue";

import { register } from "../services/auth";

const emit = defineEmits([
  "register-success",
  "switch-panel",
  "input-focus",
  "input-blur",
  "btn-enter",
  "btn-leave",
]);

const form = reactive({
  username: "",
  nickname: "",
  email: "",
  password: "",
  confirmPassword: "",
});
const submitting = ref(false);
const errorMessage = ref("");
const successMessage = ref("");

async function handleSubmit() {
  if (!form.username || !form.nickname || !form.email || !form.password) {
    errorMessage.value = "请填写所有字段。";
    successMessage.value = "";
    return;
  }

  if (form.password !== form.confirmPassword) {
    errorMessage.value = "两次输入的密码不一致。";
    successMessage.value = "";
    return;
  }

  submitting.value = true;
  errorMessage.value = "";
  successMessage.value = "";

  try {
    await register({
      username: form.username,
      nickname: form.nickname,
      email: form.email,
      password: form.password,
    });
    successMessage.value = "注册成功，正在进入工作台。";
    emit("register-success");
  } catch (error) {
    errorMessage.value =
      error?.response?.data?.detail || "注册失败，请稍后重试。";
  } finally {
    submitting.value = false;
  }
}
</script>

<style scoped>
.register-card {
  width: 100%;
  padding: 28px 28px 30px;
}

.register-card-top {
  position: relative;
  z-index: 1;
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 16px;
}

.register-card-kicker {
  margin: 0 0 8px;
  font-size: 13px;
  color: rgba(71, 85, 105, 0.7);
}

.register-card h3 {
  margin: 0;
  font-size: 42px;
  line-height: 1;
}

.register-form {
  position: relative;
  z-index: 1;
  margin-top: 26px;
  display: grid;
  gap: 16px;
}

.field {
  display: grid;
  gap: 10px;
}

.field span {
  font-size: 13px;
  color: rgba(51, 65, 85, 0.74);
  text-transform: uppercase;
}

.field input {
  width: 100%;
  min-height: 52px;
  padding: 0 18px;
  font-size: 16px;
  color: #0f172a;
  background: rgba(255, 255, 255, 0.18);
  border: 1px solid rgba(255, 255, 255, 0.32);
  border-radius: 16px;
  box-shadow:
    inset 0 1px 0 rgba(255, 255, 255, 0.4),
    0 6px 16px rgba(148, 163, 184, 0.06);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  outline: none;
  transition: border-color 160ms ease, box-shadow 160ms ease, background 160ms ease;
}

.field input:focus {
  border-color: rgba(59, 130, 246, 0.45);
  background: rgba(255, 255, 255, 0.28);
  box-shadow:
    0 0 0 3px rgba(96, 165, 250, 0.12),
    0 12px 24px rgba(96, 165, 250, 0.1);
}

.feedback {
  min-height: 20px;
  margin: 0;
  font-size: 14px;
}

.error-text {
  color: #b91c1c;
}

.success-text {
  color: #166534;
}

.card-switch-links {
  position: relative;
  z-index: 1;
  margin-top: 18px;
  text-align: center;
}

.card-switch-links a {
  font-size: 14px;
  color: rgba(59, 130, 246, 0.8);
  transition: color 160ms ease;
}

.card-switch-links a:hover {
  color: #2563eb;
}

@media (max-width: 640px) {
  .register-card {
    padding: 24px 20px;
  }

  .register-card h3 {
    font-size: 36px;
  }
}
</style>
