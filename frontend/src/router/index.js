import { createRouter, createWebHistory } from "vue-router";
import { getStoredAuthState } from "../services/auth";
import LoginView from "../views/LoginView.vue";
import ResetPasswordView from "../views/ResetPasswordView.vue";
import WorkspaceView from "../views/WorkspaceView.vue";

const router = createRouter({
  history: createWebHistory(),
  routes: [
    // === 共享层：认证与全局入口 ===
    {
      path: "/",
      name: "login",
      component: LoginView,
    },
    {
      path: "/reset-password",
      name: "reset-password",
      component: ResetPasswordView,
    },
    {
      path: "/workspace",
      name: "workspace",
      component: WorkspaceView,
      meta: {
        requiresAuth: true,
      },
    },

    // === video App ===
    // 新增 video 页面路由时放这里

    // === blog App ===
    // 新增 blog 页面路由时放这里

    // === tools App ===
    // 新增 tools 页面路由时放这里
  ],
});

router.beforeEach((to) => {
  const authState = getStoredAuthState();

  if (to.meta.requiresAuth && !authState?.accessToken) {
    return { name: "login" };
  }

  if (to.name === "login" && authState?.accessToken) {
    return { name: "workspace" };
  }

  return true;
});

export default router;
