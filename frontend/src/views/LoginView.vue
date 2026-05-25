<template>
  <div class="login-scene" :class="`login-scene--${activePanel}`">
    <div class="bg-blob bg-blob-a" />
    <div class="bg-blob bg-blob-b" />
    <div class="bg-blob bg-blob-c" />

    <div class="login-stage">
      <div class="login-brand">
        <span class="brand-dot" />
        <span class="brand-name">Serenova</span>
      </div>

      <div class="auth-viewport" :style="viewportStyle">
        <div class="auth-track" :style="trackStyle">
          <div :ref="el => sceneRefs[0] = el" class="auth-scene">
            <RegisterFormCard
              @register-success="handleSuccess"
              @switch-panel="switchPanel"
              @input-focus="onInputFocus"
              @input-blur="onInputBlur"
              @btn-enter="onBtnEnter"
              @btn-leave="onBtnLeave"
            />
          </div>

          <div :ref="el => sceneRefs[1] = el" class="auth-scene">
            <LoginFormCard
              @login-success="handleSuccess"
              @switch-panel="switchPanel"
              @input-focus="onInputFocus"
              @input-blur="onInputBlur"
              @btn-enter="onBtnEnter"
              @btn-leave="onBtnLeave"
            />
          </div>

          <div :ref="el => sceneRefs[2] = el" class="auth-scene">
            <ForgotPasswordCard
              @switch-panel="switchPanel"
              @input-focus="onInputFocus"
              @input-blur="onInputBlur"
              @btn-enter="onBtnEnter"
              @btn-leave="onBtnLeave"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, nextTick, onMounted, ref } from "vue";
import { useRouter } from "vue-router";

import ForgotPasswordCard from "../components/ForgotPasswordCard.vue";
import LoginFormCard from "../components/LoginFormCard.vue";
import RegisterFormCard from "../components/RegisterFormCard.vue";
import { useLiquidGlass } from "../composables/useLiquidGlass";

const router = useRouter();
const liquid = useLiquidGlass();

const panelOrder = ["register", "login", "forgot"];
const activePanel = ref("login");
const viewportHeight = ref(0);
const sceneRefs = ref([]);

const trackStyle = computed(() => {
  const idx = panelOrder.indexOf(activePanel.value);
  return {
    transform: `translateX(-${idx * 100}%)`,
  };
});

const viewportStyle = computed(() => ({
  height: viewportHeight.value ? `${viewportHeight.value}px` : "auto",
}));

function measureHeight() {
  const idx = panelOrder.indexOf(activePanel.value);
  const el = sceneRefs.value[idx];
  if (el) {
    viewportHeight.value = el.scrollHeight;
  }
}

function switchPanel(target) {
  if (target === activePanel.value) return;
  activePanel.value = target;
  nextTick(measureHeight);
  liquid.pulse(1.6, 600);
}

function handleSuccess() {
  router.push({ name: "workspace" });
}

onMounted(() => {
  nextTick(measureHeight);
});

function onInputFocus() {
  liquid.distort(1.12);
}

function onInputBlur() {
  liquid.settle();
}

function onBtnEnter() {
  liquid.distort(1.2);
}

function onBtnLeave() {
  liquid.settle();
}
</script>

<style scoped>
.login-scene {
  position: relative;
  width: 100%;
  height: 100vh;
  overflow: hidden;
  background: linear-gradient(145deg, #dff0ff 0%, #e8f4ff 28%, #f0e8ff 58%, #dceeff 100%);
}

/* 背景色块也跟着场景移动 */
.login-scene .bg-blob {
  transition: transform 800ms cubic-bezier(0.23, 1, 0.32, 1);
}

.login-scene--register .bg-blob-a { transform: translate(80px, -40px); }
.login-scene--register .bg-blob-b { transform: translate(-60px, 50px); }
.login-scene--register .bg-blob-c { transform: translate(40px, -30px); }

.login-scene--login .bg-blob-a { transform: translate(0, 0); }
.login-scene--login .bg-blob-b { transform: translate(0, 0); }
.login-scene--login .bg-blob-c { transform: translate(0, 0); }

.login-scene--forgot .bg-blob-a { transform: translate(-80px, 40px); }
.login-scene--forgot .bg-blob-b { transform: translate(60px, -50px); }
.login-scene--forgot .bg-blob-c { transform: translate(-40px, 30px); }

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

.bg-blob-c {
  width: 360px;
  height: 360px;
  bottom: 120px;
  left: 36%;
  background: radial-gradient(circle, rgba(160, 230, 210, 0.48), transparent 70%);
}

.login-stage {
  position: relative;
  z-index: 1;
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
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

.auth-viewport {
  width: min(440px, calc(100vw - 40px));
  overflow: hidden;
  border-radius: 28px;
  /* 用 clip-path 裁剪，避免 backdrop-filter 子元素破坏 overflow:hidden */
  clip-path: inset(0 round 28px);
  transition: height 500ms cubic-bezier(0.23, 1, 0.32, 1);
}

.auth-track {
  display: flex;
  align-items: flex-start;
  transition: transform 600ms cubic-bezier(0.23, 1, 0.32, 1);
  will-change: transform;
}

.auth-scene {
  flex: 0 0 100%;
  width: 100%;
  /* 防止内容高度影响到兄弟 scene */
  min-width: 0;
}

@media (max-width: 480px) {
  .login-brand {
    font-size: 12px;
  }
}
</style>
