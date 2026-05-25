<template>
  <section class="glass-panel forgot-card">
    <div class="forgot-card-top">
      <div>
        <p class="forgot-card-kicker">密码重置</p>
        <h3>忘记密码</h3>
      </div>
    </div>

    <div class="forgot-card-copy">
      <p>输入注册时使用的邮箱，我们将发送重置链接到你的邮箱。</p>
    </div>

    <form class="forgot-form" @submit.prevent="handleSubmit">
      <label class="field">
        <span>邮箱</span>
        <input
          v-model.trim="form.email"
          type="email"
          name="email"
          autocomplete="email"
          placeholder="请输入注册邮箱"
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
        {{ submitting ? "发送中..." : "发送重置链接" }}
      </button>
    </form>

    <div class="card-switch-links">
      <a href="#" @click.prevent="$emit('switch-panel', 'login')">返回登录</a>
    </div>
  </section>
</template>

<script setup>
import { reactive, ref } from "vue";

import { forgotPassword } from "../../services/auth";

const emit = defineEmits([
  "switch-panel",
  "input-focus",
  "input-blur",
  "btn-enter",
  "btn-leave",
]);

const form = reactive({ email: "" });
const submitting = ref(false);
const errorMessage = ref("");
const successMessage = ref("");

async function handleSubmit() {
  if (!form.email) {
    errorMessage.value = "请输入邮箱地址。";
    successMessage.value = "";
    return;
  }

  submitting.value = true;
  errorMessage.value = "";
  successMessage.value = "";

  try {
    await forgotPassword({ email: form.email });
    successMessage.value = "如果该邮箱已注册，重置链接已发送到你的邮箱。";
  } catch (error) {
    errorMessage.value =
      error?.response?.data?.detail || "发送失败，请稍后重试。";
  } finally {
    submitting.value = false;
  }
}
</script>

<style scoped>
.forgot-card {
  width: 100%;
  padding: 28px 28px 30px;
}

.forgot-card-top {
  position: relative;
  z-index: 1;
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 16px;
}

.forgot-card-kicker {
  margin: 0 0 8px;
  font-size: 13px;
  color: rgba(71, 85, 105, 0.7);
}

.forgot-card h3 {
  margin: 0;
  font-size: 42px;
  line-height: 1;
}

.forgot-card-copy {
  position: relative;
  z-index: 1;
  margin-top: 16px;
}

.forgot-card-copy p {
  margin: 0;
  max-width: 420px;
  color: rgba(51, 65, 85, 0.76);
  line-height: 1.65;
}

.forgot-form {
  position: relative;
  z-index: 1;
  margin-top: 24px;
  display: grid;
  gap: 18px;
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
  min-height: 56px;
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
  .forgot-card {
    padding: 24px 20px;
  }

  .forgot-card h3 {
    font-size: 36px;
  }
}
</style>
