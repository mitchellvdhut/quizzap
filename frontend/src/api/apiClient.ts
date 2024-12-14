// apiClient.ts
import axios from 'axios';
import type { AxiosInstance, AxiosRequestConfig, AxiosResponse } from 'axios';
class ApiClient {
  private instance: AxiosInstance;

  constructor(baseURL: string, config?: AxiosRequestConfig) {
    this.instance = axios.create({
      baseURL,
      ...config, // Allow overriding default config
    });

    // Add interceptors for request/response handling if needed
    this.instance.interceptors.request.use((config) => {
      // e.g., Add auth token
      return config;
    });

    this.instance.interceptors.response.use(
      (response) => response,
      (error) => {
        // Handle errors globally
        return Promise.reject(error);
      }
    );
  }

  public async get<T>(url: string, config?: AxiosRequestConfig): Promise<T> {
    const response: AxiosResponse<T> = await this.instance.get(url, config);
    return response.data;
  }

  public async post<T, B>(url: string, data?: B, config?: AxiosRequestConfig): Promise<T> {
    const response: AxiosResponse<T> = await this.instance.post(url, data, config);
    return response.data;
  }

  public async delete<T>(url: string, config?: AxiosRequestConfig): Promise<T> {
    const response: AxiosResponse<T> = await this.instance.delete(url, config);
    return response.data;
  }

  // Add other methods (put, delete, patch) as needed
}

export default ApiClient;
