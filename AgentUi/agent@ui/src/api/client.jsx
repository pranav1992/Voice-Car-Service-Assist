import axios from "axios";

// Ensure base URL and timeout are always set so requests don't hang indefinitely
const baseURL =
  import.meta.env.VITE_APP_BASE_URL || "http://127.0.0.1:8000";
const timeout =
  Number(import.meta.env.VITE_APP_API_TIMEOUT) > 0
    ? Number(import.meta.env.VITE_APP_API_TIMEOUT)
    : 10000; // 10s default

export const apiClient = axios.create({
  baseURL,
  timeout,
});
