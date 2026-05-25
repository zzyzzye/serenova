/**
 * 全局液态玻璃 composable。
 * 基于 SVG feDisplacementMap 滤镜，按需驱动动画循环。
 * 单例模式 — 整个应用共享一个动画引擎实例。
 */

let dispEl = null;
let currentScale = 1;
let targetScale = 1;
let isRunning = false;
const LERP_SPEED = 0.12;
const THRESHOLD = 0.001;

function tick() {
  currentScale += (targetScale - currentScale) * LERP_SPEED;

  if (Math.abs(targetScale - currentScale) < THRESHOLD) {
    currentScale = targetScale;
    dispEl.setAttribute("scale", currentScale);
    isRunning = false;
    return;
  }

  dispEl.setAttribute("scale", currentScale);
  requestAnimationFrame(tick);
}

function ensureRunning() {
  if (!isRunning && dispEl) {
    isRunning = true;
    requestAnimationFrame(tick);
  }
}

export function useLiquidGlass() {
  function init() {
    dispEl = document.getElementById("liquid-disp");
    if (!dispEl) {
      console.warn("[useLiquidGlass] 未找到 #liquid-disp 元素");
    }
  }

  function distort(target) {
    targetScale = target;
    ensureRunning();
  }

  function settle() {
    targetScale = 1;
    ensureRunning();
  }

  function pulse(peak = 1.6, duration = 600) {
    distort(peak);
    setTimeout(() => {
      settle();
    }, duration * 0.4);
  }

  return { init, distort, settle, pulse };
}
