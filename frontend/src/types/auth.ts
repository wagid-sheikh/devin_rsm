export interface LoginRequest {
  email: string;
  password: string;
}

export interface TokenResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
}

export interface RefreshRequest {
  refresh_token: string;
}

export interface RefreshResponse {
  access_token: string;
  token_type: string;
}

export interface LogoutRequest {
  refresh_token?: string;
}

export interface RoleResponse {
  id: number;
  code: string;
  name: string;
  description: string | null;
  permissions: Record<string, unknown>;
}

export interface UserResponse {
  id: number;
  email: string;
  phone: string | null;
  first_name: string;
  last_name: string;
  status: string;
  roles: RoleResponse[];
  created_at: string;
  updated_at: string;
}
