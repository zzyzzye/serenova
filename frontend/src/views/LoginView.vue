<template>
  <div class="login-scene">
    <section class="glass-stage">
      <div class="wallpaper-layer wallpaper-layer-a" />
      <div class="wallpaper-layer wallpaper-layer-b" />
      <div class="wallpaper-layer wallpaper-layer-c" />

      <div class="status-bar">
        <span>21:29</span>
        <div class="status-icons">
          <span class="status-dot" />
          <span class="status-dot" />
          <span class="status-pill">47</span>
        </div>
      </div>

      <div class="widget-panel glass-panel">
        <div class="widget-main">
          <div class="avatar-badge">Z</div>
          <div>
            <strong>2h 1m</strong>
            <span>控制台在线时长</span>
          </div>
        </div>
        <div class="widget-chart">
          <span />
          <span />
          <span />
          <span />
        </div>
        <div class="widget-side">
          <div><b>30m</b><span>上传</span></div>
          <div><b>19m</b><span>审核</span></div>
          <div><b>12m</b><span>发布</span></div>
        </div>
      </div>

      <div class="app-grid">
        <article v-for="app in apps" :key="app.name" class="app-tile">
          <div class="app-icon" :class="app.theme">
            <span>{{ app.symbol }}</span>
          </div>
          <span>{{ app.name }}</span>
        </article>
      </div>

      <div class="search-bubble glass-chip">Search</div>

      <div class="dock glass-panel">
        <div v-for="app in dockApps" :key="app.name" class="dock-icon" :class="app.theme">
          <span>{{ app.symbol }}</span>
        </div>
      </div>

      <div class="stage-copy glass-panel">
        <p class="stage-kicker">Video OS</p>
        <h2>液态玻璃登录入口</h2>
        <p>像系统主屏一样悬浮、通透、柔和，但仍然是能干活的后台登录页。</p>
      </div>
    </section>

    <aside class="login-overlay">
      <div class="overlay-intro">
        <div class="login-badge glass-chip">Secure console access</div>
        <h1>登录控制台</h1>
        <p>账号登录、会话存储、令牌校验，都收在这块悬浮玻璃里。</p>
      </div>
      <LoginFormCard @login-success="handleLoginSuccess" />
    </aside>
  </div>
</template>

<script setup>
import { useRouter } from "vue-router";

import LoginFormCard from "../components/LoginFormCard.vue";

const router = useRouter();

const apps = [
  { name: "直播", symbol: "◉", theme: "theme-green" },
  { name: "音乐", symbol: "♪", theme: "theme-pink" },
  { name: "镜头", symbol: "◌", theme: "theme-dark" },
  { name: "消息", symbol: "✉", theme: "theme-blue" },
  { name: "稿件", symbol: "≡", theme: "theme-yellow" },
  { name: "提醒", symbol: "•", theme: "theme-soft" },
  { name: "首页", symbol: "⌂", theme: "theme-orange" },
  { name: "天气", symbol: "☁", theme: "theme-sky" },
];

const dockApps = [
  { name: "通话", symbol: "◐", theme: "theme-lime" },
  { name: "聊天", symbol: "◎", theme: "theme-green" },
  { name: "浏览", symbol: "◍", theme: "theme-cyan" },
  { name: "相册", symbol: "✿", theme: "theme-rainbow" },
];

function handleLoginSuccess() {
  router.push({ name: "workspace" });
}
</script>

<style scoped>
.login-scene {
  min-height: 100vh;
  display: grid;
  grid-template-columns: minmax(0, 1.18fr) minmax(360px, 440px);
  gap: 28px;
  padding: 22px;
  position: relative;
}

.glass-stage {
  position: relative;
  min-height: calc(100vh - 44px);
  padding: 26px 28px 34px;
  overflow: hidden;
  border-radius: 38px;
  background:
    linear-gradient(135deg, rgba(191, 245, 240, 0.88), rgba(74, 144, 226, 0.18) 38%, rgba(27, 78, 193, 0.16) 64%, rgba(234, 245, 255, 0.62) 100%);
  box-shadow:
    inset 0 1px 0 rgba(255, 255, 255, 0.75),
    0 30px 90px rgba(91, 127, 188, 0.28);
}

.wallpaper-layer {
  position: absolute;
  border-radius: 999px;
  pointer-events: none;
}

.wallpaper-layer-a {
  width: 760px;
  height: 760px;
  left: -180px;
  bottom: -220px;
  background: linear-gradient(145deg, rgba(131, 246, 217, 0.78), rgba(154, 230, 244, 0.3) 42%, rgba(245, 250, 255, 0.08) 78%);
  border: 2px solid rgba(255, 255, 255, 0.34);
}

.wallpaper-layer-b {
  width: 560px;
  height: 880px;
  right: 120px;
  top: -140px;
  background: linear-gradient(180deg, rgba(6, 28, 96, 0.84), rgba(18, 96, 220, 0.44) 52%, rgba(19, 78, 186, 0.08) 100%);
  border: 1px solid rgba(255, 255, 255, 0.22);
}

.wallpaper-layer-c {
  width: 460px;
  height: 820px;
  right: -80px;
  bottom: -260px;
  background: linear-gradient(160deg, rgba(234, 243, 255, 0.7), rgba(197, 223, 255, 0.18) 52%, rgba(255, 255, 255, 0.1) 82%);
  border: 1px solid rgba(255, 255, 255, 0.32);
}

.status-bar {
  position: relative;
  z-index: 1;
  display: flex;
  align-items: center;
  justify-content: space-between;
  color: rgba(255, 255, 255, 0.96);
  font-weight: 600;
  font-size: 18px;
  padding: 2px 4px;
}

.status-icons {
  display: flex;
  align-items: center;
  gap: 10px;
}

.status-dot {
  width: 9px;
  height: 9px;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.92);
}

.status-pill {
  padding: 4px 10px;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.22);
  border: 1px solid rgba(255, 255, 255, 0.3);
  font-size: 14px;
}

.widget-panel {
  position: relative;
  z-index: 1;
  margin-top: 36px;
  width: min(720px, 82%);
  min-height: 220px;
  padding: 28px 30px;
  display: grid;
  grid-template-columns: minmax(0, 1.15fr) 220px;
  gap: 24px;
}

.widget-panel::after {
  content: "";
  position: absolute;
  top: 0;
  bottom: 0;
  right: 220px;
  width: 1px;
  background: rgba(255, 255, 255, 0.22);
}

.widget-main {
  display: flex;
  align-items: center;
  gap: 18px;
}

.avatar-badge {
  width: 54px;
  height: 54px;
  border-radius: 999px;
  display: grid;
  place-items: center;
  font-size: 24px;
  color: white;
  background: linear-gradient(180deg, rgba(255, 122, 198, 0.95), rgba(244, 114, 182, 0.72));
  box-shadow: 0 14px 24px rgba(244, 114, 182, 0.24);
}

.widget-main strong {
  display: block;
  font-size: 56px;
  line-height: 1;
  color: rgba(255, 255, 255, 0.98);
}

.widget-main span,
.widget-side span {
  color: rgba(255, 255, 255, 0.78);
}

.widget-chart {
  margin-top: 28px;
  min-height: 84px;
  border-radius: 18px;
  border: 1px solid rgba(255, 255, 255, 0.16);
  display: flex;
  align-items: flex-end;
  gap: 18px;
  padding: 18px;
  background:
    linear-gradient(180deg, rgba(255, 255, 255, 0.08), rgba(255, 255, 255, 0.02)),
    repeating-linear-gradient(to right, transparent 0 86px, rgba(255, 255, 255, 0.08) 86px 87px);
}

.widget-chart span {
  width: 16px;
  border-radius: 999px 999px 6px 6px;
  background: linear-gradient(180deg, rgba(255, 255, 255, 0.82), rgba(244, 114, 182, 0.72) 58%, rgba(250, 204, 21, 0.76) 100%);
}

.widget-chart span:nth-child(1) { height: 18px; }
.widget-chart span:nth-child(2) { height: 52px; }
.widget-chart span:nth-child(3) { height: 12px; }
.widget-chart span:nth-child(4) { height: 64px; }

.widget-side {
  display: grid;
  gap: 18px;
  align-content: start;
  padding-top: 12px;
}

.widget-side div {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  color: rgba(255, 255, 255, 0.96);
}

.widget-side b {
  font-size: 24px;
  font-weight: 500;
}

.app-grid {
  position: relative;
  z-index: 1;
  margin-top: 42px;
  width: min(720px, 82%);
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 108px));
  gap: 28px 26px;
}

.app-tile {
  display: grid;
  justify-items: center;
  gap: 10px;
  color: rgba(255, 255, 255, 0.94);
}

.app-icon,
.dock-icon {
  position: relative;
  width: 92px;
  height: 92px;
  display: grid;
  place-items: center;
  border-radius: 24px;
  background: linear-gradient(180deg, rgba(255, 255, 255, 0.34), rgba(255, 255, 255, 0.14));
  border: 1px solid rgba(255, 255, 255, 0.34);
  box-shadow:
    inset 0 1px 0 rgba(255, 255, 255, 0.72),
    0 24px 34px rgba(50, 86, 150, 0.18);
  backdrop-filter: blur(18px) saturate(165%);
  -webkit-backdrop-filter: blur(18px) saturate(165%);
}

.app-icon::before,
.dock-icon::before {
  content: "";
  position: absolute;
  inset: 6px;
  border-radius: 20px;
  background: var(--icon-bg, linear-gradient(180deg, rgba(255, 255, 255, 0.66), rgba(255, 255, 255, 0.2)));
}

.app-icon span,
.dock-icon span {
  position: relative;
  z-index: 1;
  font-size: 34px;
  color: white;
  text-shadow: 0 3px 10px rgba(0, 0, 0, 0.12);
}

.app-tile > span {
  font-size: 14px;
  text-shadow: 0 3px 14px rgba(18, 41, 98, 0.26);
}

.theme-green { --icon-bg: linear-gradient(180deg, #73f6b3, #22c55e); }
.theme-pink { --icon-bg: linear-gradient(180deg, #ff7ab6, #ec4899); }
.theme-dark { --icon-bg: linear-gradient(180deg, #344256, #0f172a); }
.theme-blue { --icon-bg: linear-gradient(180deg, #7fc3ff, #2563eb); }
.theme-yellow { --icon-bg: linear-gradient(180deg, #fde047, #facc15); }
.theme-soft { --icon-bg: linear-gradient(180deg, #c7d2fe, #93c5fd); }
.theme-orange { --icon-bg: linear-gradient(180deg, #fdba74, #f59e0b); }
.theme-sky { --icon-bg: linear-gradient(180deg, #dbeafe, #60a5fa); }
.theme-lime { --icon-bg: linear-gradient(180deg, #86efac, #22c55e); }
.theme-cyan { --icon-bg: linear-gradient(180deg, #67e8f9, #38bdf8); }
.theme-rainbow { --icon-bg: linear-gradient(135deg, #fb7185, #f59e0b 35%, #fde047 58%, #4ade80 76%, #60a5fa 100%); }

.search-bubble {
  position: relative;
  z-index: 1;
  margin: 34px auto 0;
  font-size: 24px;
  color: rgba(255, 255, 255, 0.86);
  padding-inline: 24px;
  min-height: 54px;
  display: inline-flex;
  justify-content: center;
}

.dock {
  position: absolute;
  left: 32px;
  right: 32px;
  bottom: 24px;
  z-index: 1;
  width: auto;
  display: flex;
  justify-content: center;
  gap: 18px;
  padding: 16px 22px;
  border-radius: 30px;
}

.dock-icon {
  width: 86px;
  height: 86px;
  border-radius: 22px;
}

.stage-copy {
  position: absolute;
  right: 26px;
  bottom: 154px;
  z-index: 2;
  width: 320px;
  padding: 22px 24px;
}

.stage-kicker {
  margin: 0 0 10px;
  font-size: 12px;
  text-transform: uppercase;
  color: rgba(255, 255, 255, 0.76);
}

.stage-copy h2 {
  margin: 0;
  font-size: 30px;
  line-height: 1.1;
  color: white;
}

.stage-copy p {
  margin: 12px 0 0;
  color: rgba(255, 255, 255, 0.82);
  line-height: 1.6;
}

.login-overlay {
  position: relative;
  z-index: 3;
  display: grid;
  align-content: center;
  gap: 20px;
  padding: 22px 10px 22px 0;
}

.overlay-intro {
  padding: 0 12px;
  color: #0f172a;
}

.glass-chip {
  width: fit-content;
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 10px 16px;
  border-radius: 999px;
  border: 1px solid rgba(255, 255, 255, 0.42);
  background: linear-gradient(180deg, rgba(255, 255, 255, 0.36), rgba(255, 255, 255, 0.18));
  box-shadow:
    0 18px 36px rgba(114, 138, 183, 0.16),
    inset 0 1px 0 rgba(255, 255, 255, 0.65);
  backdrop-filter: blur(22px) saturate(150%);
  -webkit-backdrop-filter: blur(22px) saturate(150%);
}

.login-badge {
  font-size: 13px;
  color: rgba(30, 64, 175, 0.82);
}

.overlay-intro h1 {
  margin: 18px 0 0;
  font-size: 52px;
  line-height: 0.98;
}

.overlay-intro p {
  margin: 16px 0 0;
  font-size: 18px;
  line-height: 1.7;
  color: rgba(51, 65, 85, 0.84);
}

@media (max-width: 1160px) {
  .login-scene {
    grid-template-columns: 1fr;
    padding: 18px;
  }

  .glass-stage {
    min-height: 900px;
  }

  .login-overlay {
    padding: 0 0 18px;
  }
}

@media (max-width: 820px) {
  .widget-panel,
  .app-grid {
    width: 100%;
  }

  .widget-panel {
    grid-template-columns: 1fr;
  }

  .widget-panel::after,
  .stage-copy {
    display: none;
  }

  .app-grid {
    grid-template-columns: repeat(4, minmax(0, 1fr));
  }
}

@media (max-width: 640px) {
  .login-scene {
    padding: 0;
  }

  .glass-stage {
    min-height: auto;
    border-radius: 0;
    padding: 20px 18px 140px;
  }

  .widget-main strong {
    font-size: 42px;
  }

  .app-grid {
    gap: 18px 14px;
  }

  .app-icon,
  .dock-icon {
    width: 72px;
    height: 72px;
  }

  .dock {
    left: 16px;
    right: 16px;
    bottom: 18px;
    gap: 12px;
    padding-inline: 14px;
  }

  .overlay-intro {
    padding-inline: 18px;
  }

  .overlay-intro h1 {
    font-size: 42px;
  }
}
</style>
