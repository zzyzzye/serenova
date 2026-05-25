<template>
  <div class="reset-scene">
    <div class="bg-blob bg-blob-a" />
    <div class="bg-blob bg-blob-b" />

    <div class="reset-center">
      <div class="login-brand">
        <span class="brand-dot" />
        <span class="brand-name">Serenova</span>
      </div>

      <section class="glass-panel reset-card">
        <div class="reset-card-top">
          <div>
            <p class="reset-card-kicker">密码重置</p>
            <h3>设置新密码</h3>
          </div>
        </div>

        <div v-if="!token" class="reset-card-copy">
          <p class="error-text">重置链接无效或已过期，请重新发起忘记密码流程。</p>
          <button class="ghost-button" type="button" @click="goLogin">返回登录</button>
        </div>

        <form v-else class="reset-form" @submit.prevent="handleSubmit">
          <label class="field">
            <span>新密码</span>
            <input
              v-model="form.password"
              type="password"
              name="new-password"
              autocomplete="new-password"
              placeholder="至少 6 个字符"
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
            />
          </label>

          <p v-if="errorMessage" class="feedback error-text">{{ errorMessage }}</p>
          <p v-else-if="successMessage" class="feedback success-text">{{ successMessage }}</p>

          <button class="primary-button" type="submit" :disabled="submitting">
            {{ submitting ? "重置中..." : "重置密码" }}
          </button>
        </form>
      </section>
    </div>
  </div>
</template>

<script setup>
import { computed, reactive, ref } from "vue";
import { useRoute, useRouter } from "vue-router";

import { resetPassword } from "../services/auth";

const route = useRoute();
const router = useRouter();

const token = computed(() => route.query.token || "");

const form = reactive({
  password: "",
  confirmPassword: "",
});
const submitting = ref(false);
const errorMessage = ref("");
const successMessage = ref("");

function goLogin() {
  router.push({ name: "login" });
}

async function handleSubmit() {
  if (!form.password || form.password.length < 6) {
    errorMessage.value = "密码至少需要 6 个字符。";
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
    await resetPassword({ token: token.value, new_password: form.password });
    successMessage.value = "密码已重置，3 秒后跳转到登录页。";
    setTimeout(() => {
      router.push({ name: "login" });
    }, 3000);
  } catch (error) {
    errorMessage.value =
      error?.response?.data?.detail || "重置失败，请重新发起忘记密码流程。";
  } finally {
    submitting.value = false;
  }
}
</script>

<style scoped>
.reset-scene {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
  background: linear-gradient(145deg, #dff0ff 0%, #e8f4ff 28%, #f0e8ff 58%, #dceeff 100%);
}

.bg-blob {
  position: absolute;
  border-radius: 999px;
  pointer-events: none;
  filter: blur(72px);
  opacity: 0.55;
}

.bg-blob-a {
  width: 680px;
  height: 680px;
  top: -160px;
  left: -120px;
  background: radial-gradient(circle, rgba(120, 200, 255, 0.72), rgba(160, 220, 255, 0.22) 68%, transparent 100%);
}

.bg-blob-b {
  width: 520px;
  height: 520px;
  bottom: -100px;
  right: -80px;
  background: radial-gradient(circle, rgba(200, 170, 255, 0.62), rgba(210, 195, 255, 0.18) 64%, transparent 100%);
}

.reset-center {
  position: relative;
  z-index: 1;
  width: min(420px, calc(100vw - 40px));
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
}

.login-brand {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 7px 14px;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.22);
  border: 1px solid rgba(255, 255, 255, 0.38);
  backdrop-filter: blur(20px) saturate(160%);
  -webkit-backdrop-filter: blur(20px) saturate(160%);
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.45), 0 6px 20px rgba(120, 160, 220, 0.1);
  margin-bottom: 10px;
}

.brand-dot {
  width: 9px;
  height: 9px;
  border-radius: 999px;
  background: radial-gradient(circle at 30% 30%, #ffffff 0%, #93c5fd 38%, #3b82f6 100%);
  box-shadow: 0 0 8px rgba(59, 130, 246, 0.5);
}

.brand-name {
  font-size: 13px;
  font-weight: 600;
  color: rgba(30, 64, 175, 0.8);
  letter-spacing: 0.04em;
}

.reset-card {
  width: 100%;
  padding: 28px 28px 30px;
}

.reset-card-top {
  position: relative;
  z-index: 1;
}

.reset-card-kicker {
  margin: 0 0 8px;
  font-size: 13px;
  color: rgba(71, 85, 105, 0.7);
}

.reset-card h3 {
  margin: 0;
  font-size: 38px;
  line-height: 1;
}

.reset-card-copy {
  position: relative;
  z-index: 1;
  margin-top: 20px;
  display: grid;
  gap: 16px;
}

.reset-card-copy p {
  margin: 0;
  line-height: 1.65;
}

.reset-form {
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
</style>
