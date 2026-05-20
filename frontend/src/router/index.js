import { createRouter, createWebHistory } from "vue-router";
import { getStoredAuthState } from "../services/auth";
import LoginView from "../views/LoginView.vue";
import WorkspaceView from "../views/WorkspaceView.vue";

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: "/",
      name: "login",
      component: LoginView,
    },
    {
      path: "/workspace",
      name: "workspace",
      component: WorkspaceView,
      meta: {
        requiresAuth: true,
      },
    },
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
