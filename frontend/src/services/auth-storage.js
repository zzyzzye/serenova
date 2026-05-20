const AUTH_STORAGE_KEY = "video.auth";

export function persistAuthState(data) {
  const authState = {
    accessToken: data.access_token || data.accessToken,
    refreshToken: data.refresh_token || data.refreshToken,
    user: data.user,
    accessTokenExpiresAt: data.access_token_expires_at || data.accessTokenExpiresAt,
    refreshTokenExpiresAt: data.refresh_token_expires_at || data.refreshTokenExpiresAt,
  };
  localStorage.setItem(AUTH_STORAGE_KEY, JSON.stringify(authState));
}

export function getStoredAuthState() {
  const rawValue = localStorage.getItem(AUTH_STORAGE_KEY);
  if (!rawValue) {
    return null;
  }
  try {
    return JSON.parse(rawValue);
  } catch (error) {
    localStorage.removeItem(AUTH_STORAGE_KEY);
    return null;
  }
}

export function clearAuthState() {
  localStorage.removeItem(AUTH_STORAGE_KEY);
}
