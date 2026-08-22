import { ApiError } from "./api";

export function getErrorMessage(
  error: unknown,
  fallback = "Something went wrong"
): string {
  if (error instanceof ApiError) {
    return error.detail;
  }
  if (error instanceof Error) {
    return error.message;
  }
  return fallback;
}