import axios from "axios";
import { getStoredAuthState } from "./auth-storage";

const http = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000/api/v1",
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
