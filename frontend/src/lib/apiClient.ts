import { OpenAPI } from './sdk/core/OpenAPI';
import { AuthService, CompaniesService, StoresService } from './sdk';
import type { LoginRequest, RefreshRequest, LogoutRequest } from './sdk';

const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL as string | undefined) || 'http://localhost:8000/api/v1';

OpenAPI.BASE = API_BASE_URL;

export class ApiClient {
  private static accessToken: string | null = null;

  static setAccessToken(token: string | null) {
    this.accessToken = token;
    OpenAPI.TOKEN = token || undefined;
  }

  static getAccessToken(): string | null {
    return this.accessToken;
  }

  static auth = {
    login: async (credentials: LoginRequest) => {
      return AuthService.loginApiV1AuthLoginPost(credentials);
    },
    
    refresh: async (data: RefreshRequest) => {
      return AuthService.refreshApiV1AuthRefreshPost(data);
    },
    
    logout: async (data: LogoutRequest) => {
      return AuthService.logoutApiV1AuthLogoutPost(data);
    },
    
    getMe: async () => {
      return AuthService.getCurrentUserInfoApiV1AuthMeGet();
    },
  };

  static companies = CompaniesService;
  static stores = StoresService;
}
