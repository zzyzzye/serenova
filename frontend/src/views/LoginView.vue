<template>
  <!--
    视口：固定 100vw × 100vh 的窗口，overflow:hidden 裁掉画布溢出部分
  -->
  <div class="login-viewport">
    <!--
      画布：真正的大画布，三个全屏格子按三角形摆放。
      整体平移画布，让对应格子对齐视口左上角。

      三角形布局（每格 100vw × 100vh）：
        登录   → (0,      0     )  左上
        注册   → (0,      100vh )  左下
        忘记   → (100vw,  50vh  )  右中

      平移时：translate = -(target_col_offset)
      让目标格子的左上角 = 画布原点 = 视口左上角
    -->
    <div class="login-canvas" :style="canvasStyle">

      <!-- 画布级大背景：铺满整个画布，三格共享，切换时背景不换 -->
      <div class="canvas-bg">
        <div class="canvas-blob canvas-blob-a" />
        <div class="canvas-blob canvas-blob-b" />
        <div class="canvas-blob canvas-blob-c" />
        <div class="canvas-blob canvas-blob-d" />
        <div class="canvas-blob canvas-blob-e" />
      </div>

      <!-- 登录：左上 (0, 0) -->
      <div class="login-cell" style="left:0; top:0;">
        <div class="cell-inner">
          <div class="login-brand"><span class="brand-dot" /><span class="brand-name">Serenova</span></div>
          <LoginFormCard
            @login-success="handleSuccess" @switch-panel="switchPanel"
            @input-focus="onInputFocus" @input-blur="onInputBlur"
            @btn-enter="onBtnEnter" @btn-leave="onBtnLeave"
          />
        </div>
      </div>

      <!-- 注册：左下 (0, 100vh) -->
      <div class="login-cell" style="left:0; top:100vh;">
        <div class="cell-inner">
          <div class="login-brand"><span class="brand-dot" /><span class="brand-name">Serenova</span></div>
          <RegisterFormCard
            @register-success="handleSuccess" @switch-panel="switchPanel"
            @input-focus="onInputFocus" @input-blur="onInputBlur"
            @btn-enter="onBtnEnter" @btn-leave="onBtnLeave"
          />
        </div>
      </div>

      <!-- 忘记密码：右中 (100vw, 50vh) -->
      <div class="login-cell" style="left:100vw; top:50vh;">
        <div class="cell-inner">
          <div class="login-brand"><span class="brand-dot" /><span class="brand-name">Serenova</span></div>
          <ForgotPasswordCard
            @switch-panel="switchPanel"
            @input-focus="onInputFocus" @input-blur="onInputBlur"
            @btn-enter="onBtnEnter" @btn-leave="onBtnLeave"
          />
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { computed, ref } from "vue";
import { useRouter } from "vue-router";

import ForgotPasswordCard from "../components/auth/ForgotPasswordCard.vue";
import LoginFormCard from "../components/auth/LoginFormCard.vue";
import RegisterFormCard from "../components/auth/RegisterFormCard.vue";
import { useLiquidGlass } from "../composables/useLiquidGlass";

const router = useRouter();
const liquid = useLiquidGlass();

/*
  每个格子在画布上的左上角坐标（vw/vh 单位）。
  平移画布时用 translate(-(x)vw, -(y)vh) 让该格子对齐视口左上角。
*/
const cellPos = {
  login:    { x: 0,   y: 0   },
  register: { x: 0,   y: 100 },
  forgot:   { x: 100, y: 50  },
};

const activePanel = ref("login");

const canvasStyle = computed(() => {
  const p = cellPos[activePanel.value];
  return {
    transform: `translate(${-p.x}vw, ${-p.y}vh)`,
  };
});

function switchPanel(target) {
  if (target === activePanel.value) return;
  activePanel.value = target;
  liquid.pulse(1.6, 600);
}

function handleSuccess() {
  router.push({ name: "workspace" });
}

function onInputFocus()  { liquid.distort(1.12); }
function onInputBlur()   { liquid.settle(); }
function onBtnEnter()    { liquid.distort(1.2); }
function onBtnLeave()    { liquid.settle(); }
</script>

<style scoped>
/* 视口窗口：固定 100vw×100vh，裁掉画布溢出 */
.login-viewport {
  position: fixed;
  inset: 0;
  overflow: hidden;
}

/* 大画布：不设宽高，由内容撑开，整体平移 */
.login-canvas {
  position: absolute;
  top: 0;
  left: 0;
  transition: transform 600ms cubic-bezier(0.25, 0.46, 0.45, 0.94);
  will-change: transform;
}

/* 每个格子：精确 100vw × 100vh，绝对定位在画布上 */
.login-cell {
  position: absolute;
  width: 100vw;
  height: 100vh;
  overflow: hidden;
}

/* 画布级大背景：覆盖整个 200vw×150vh 画布空间 */
.canvas-bg {
  position: absolute;
  /* 从画布原点延伸到最远格子右下角：200vw × 200vh 足够覆盖三角形 */
  top: 0; left: 0;
  width: 200vw;
  height: 200vh;
  background: linear-gradient(145deg, #ddf0ff 0%, #e8f4ff 25%, #ede8ff 55%, #e2eeff 78%, #ecdeff 100%);
  pointer-events: none;
  z-index: 0;
}

.canvas-blob {
  position: absolute;
  border-radius: 999px;
  filter: blur(90px);
  opacity: 0.6;
}
/* 左上区（登录附近） */
.canvas-blob-a {
  width: 800px; height: 800px;
  top: -200px; left: -120px;
  background: radial-gradient(circle, rgba(110,195,255,0.68), rgba(150,215,255,0.16) 65%, transparent);
}
/* 左下区（注册附近） */
.canvas-blob-b {
  width: 720px; height: 720px;
  top: calc(100vh - 100px); left: -80px;
  background: radial-gradient(circle, rgba(100,185,255,0.6), rgba(140,210,255,0.14) 65%, transparent);
}
/* 右中区（忘记密码附近） */
.canvas-blob-c {
  width: 700px; height: 700px;
  top: calc(50vh - 200px); left: calc(100vw - 100px);
  background: radial-gradient(circle, rgba(185,145,255,0.62), rgba(205,175,255,0.14) 65%, transparent);
}
/* 中间过渡光晕 */
.canvas-blob-d {
  width: 560px; height: 560px;
  top: calc(80vh); left: calc(60vw);
  background: radial-gradient(circle, rgba(160,200,255,0.42), transparent 68%);
}
/* 右下角补光 */
.canvas-blob-e {
  width: 480px; height: 480px;
  top: calc(130vh); left: calc(120vw);
  background: radial-gradient(circle, rgba(200,170,255,0.38), transparent 68%);
}

/* 每格的内容居中区 */
.cell-inner {
  position: relative;
  z-index: 1;
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 12px;
  overflow-y: auto;
  padding: 40px 20px;
  box-sizing: border-box;
}

.cell-inner > :deep(.glass-panel) {
  width: min(440px, calc(100vw - 40px));
}

.login-brand {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 7px 14px;
  border-radius: 999px;
  background: rgba(255,255,255,0.22);
  border: 1px solid rgba(255,255,255,0.38);
  backdrop-filter: blur(20px) saturate(160%);
  -webkit-backdrop-filter: blur(20px) saturate(160%);
  box-shadow: inset 0 1px 0 rgba(255,255,255,0.45), 0 6px 20px rgba(120,160,220,0.1);
  flex-shrink: 0;
}

.brand-dot {
  width: 9px; height: 9px;
  border-radius: 999px;
  background: radial-gradient(circle at 30% 30%, #fff 0%, #93c5fd 38%, #3b82f6 100%);
  box-shadow: 0 0 8px rgba(59,130,246,0.5);
}

.brand-name {
  font-size: 13px;
  font-weight: 600;
  color: rgba(30,64,175,0.8);
  letter-spacing: 0.04em;
}
</style>
