import type {
  LoginRequest,
  TokenResponse,
  RefreshRequest,
  RefreshResponse,
  LogoutRequest,
  UserResponse,
} from '@/types/auth';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1';

class ApiError extends Error {
  constructor(
    message: string,
    public status: number,
    public data?: unknown
  ) {
    super(message);
    this.name = 'ApiError';
  }
}

async function fetchApi<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const url = `${API_BASE_URL}${endpoint}`;
  
  const response = await fetch(url, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new ApiError(
      errorData.detail || 'An error occurred',
      response.status,
      errorData
    );
  }

  return response.json();
}

export const authApi = {
  login: (data: LoginRequest) =>
    fetchApi<TokenResponse>('/auth/login', {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  refresh: (data: RefreshRequest) =>
    fetchApi<RefreshResponse>('/auth/refresh', {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  logout: (data: LogoutRequest) =>
    fetchApi<{ message: string }>('/auth/logout', {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  getMe: (accessToken: string) =>
    fetchApi<UserResponse>('/auth/me', {
      headers: {
        Authorization: `Bearer ${accessToken}`,
      },
    }),
};

export { ApiError };
