import http from "./http";
import {
  clearAuthState,
  getStoredAuthState,
  persistAuthState,
} from "./auth-storage";

export async function login(payload) {
  const { data } = await http.post("/auth/login", payload);
  persistAuthState(data);
  return data;
}

export async function register(payload) {
  const { data } = await http.post("/auth/register", payload);
  persistAuthState(data);
  return data;
}

export async function forgotPassword(payload) {
  const { data } = await http.post("/auth/forgot-password", payload);
  return data;
}

export async function resetPassword(payload) {
  const { data } = await http.post("/auth/reset-password", payload);
  return data;
}

export async function fetchCurrentUser() {
  const { data } = await http.get("/auth/me");
  return data;
}

export async function logout() {
  try {
    await http.post("/auth/logout");
  } finally {
    clearAuthState();
  }
}

export { clearAuthState, getStoredAuthState, persistAuthState };
