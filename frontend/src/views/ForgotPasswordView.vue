<template>
  <!--
    忘记密码页面：独立路由页，品牌标识 + 忘记密码表单卡片。
    与登录页共享背景风格，通过路由跳转切换。
  -->
  <div class="auth-scene">
    <div class="bg-blob bg-blob-a" />
    <div class="bg-blob bg-blob-b" />

    <div class="auth-center">
      <div class="login-brand"><span class="brand-dot" /><span class="brand-name">Serenova</span></div>
      <ForgotPasswordCard
        @switch-panel="switchPanel"
        @input-focus="onInputFocus" @input-blur="onInputBlur"
        @btn-enter="onBtnEnter" @btn-leave="onBtnLeave"
      />
    </div>
  </div>
</template>

<script setup>
import { useRouter } from "vue-router";

import ForgotPasswordCard from "../components/auth/ForgotPasswordCard.vue";
import { useLiquidGlass } from "../composables/useLiquidGlass";

const router = useRouter();
const liquid = useLiquidGlass();

function switchPanel(target) {
  if (target === "login") router.push({ name: "login" });
  else if (target === "register") router.push({ name: "register" });
}

function onInputFocus()  { liquid.distort(1.12); }
function onInputBlur()   { liquid.settle(); }
function onBtnEnter()    { liquid.distort(1.2); }
function onBtnLeave()    { liquid.settle(); }
</script>

<style scoped>
.auth-scene {
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
  width: 680px; height: 680px;
  top: -160px; left: -120px;
  background: radial-gradient(circle, rgba(120, 200, 255, 0.72), rgba(160, 220, 255, 0.22) 68%, transparent 100%);
}

.bg-blob-b {
  width: 520px; height: 520px;
  bottom: -100px; right: -80px;
  background: radial-gradient(circle, rgba(200, 170, 255, 0.62), rgba(210, 195, 255, 0.18) 64%, transparent 100%);
}

.auth-center {
  position: relative;
  z-index: 1;
  width: min(440px, calc(100vw - 40px));
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
}

.brand-dot {
  width: 9px; height: 9px;
  border-radius: 999px;
  background: radial-gradient(circle at 30% 30%, #fff 0%, #93c5fd 38%, #3b82f6 100%);
  box-shadow: 0 0 8px rgba(59, 130, 246, 0.5);
}

.brand-name {
  font-size: 13px;
  font-weight: 600;
  color: rgba(30, 64, 175, 0.8);
  letter-spacing: 0.04em;
}
</style>
