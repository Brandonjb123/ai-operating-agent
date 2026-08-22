import { apiClient } from "./api";
import type { LoginRequest, RegisterRequest, TokenResponse, User } from "@/types/auth";

const TOKEN_KEY = "access_token";

export function setAccessToken(token: string): void {
  if (typeof window !== "undefined") {
    localStorage.setItem(TOKEN_KEY, token);
  }
}

export function getAccessToken(): string | null {
  if (typeof window === "undefined") return null;
  return localStorage.getItem(TOKEN_KEY);
}

export function removeAccessToken(): void {
  if (typeof window !== "undefined") {
    localStorage.removeItem(TOKEN_KEY);
  }
}

export function isAuthenticated(): boolean {
  return getAccessToken() !== null;
}

export async function login(credentials: LoginRequest): Promise<User> {
  const tokenRes = await apiClient<TokenResponse>("/auth/login", {
    method: "POST",
    body: JSON.stringify(credentials),
  });
  setAccessToken(tokenRes.access_token);
  return fetchCurrentUser();
}

export async function register(data: RegisterRequest): Promise<User> {
  const tokenRes = await apiClient<TokenResponse>("/auth/register", {
    method: "POST",
    body: JSON.stringify(data),
  });
  setAccessToken(tokenRes.access_token);
  return fetchCurrentUser();
}

export async function fetchCurrentUser(): Promise<User> {
  return apiClient<User>("/auth/me", {
    method: "GET",
  });
}

export function logout(): void {
  removeAccessToken();
  if (typeof window !== "undefined") {
    // eslint-disable-next-line @next/next/no-location-assign-relative-destination
    window.location.href = "/login";
  }
}