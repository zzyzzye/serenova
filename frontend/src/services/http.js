import axios from "axios";
import { getStoredAuthState } from "./auth-storage";

// 开发模式下直连后端，Docker 模式下使用相对路径由 nginx 代理
const defaultBaseURL = import.meta.env.DEV
  ? "http://127.0.0.1:8000/api"
  : "/api";

const http = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || defaultBaseURL,
  timeout: 8000,
});

http.interceptors.request.use((config) => {
  const authState = getStoredAuthState();
  if (authState?.accessToken) {
    config.headers.Authorization = `Bearer ${authState.accessToken}`;
  }
  return config;
});

export default http;
