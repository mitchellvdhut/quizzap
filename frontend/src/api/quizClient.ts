import ApiClient from './apiClient';
import type {Quiz} from "@/types";

const apiClient = new ApiClient('https://localhost/api/latest');

export async function getQuizzes(): Promise<Quiz[]> {
  return apiClient.get<Quiz[]>('/quizzes');
}

export async function createQuiz(name: string, description: string): Promise<Quiz> {
  return apiClient.post<Quiz, {name: string, description: string}>(`/quizzes`, {name, description});
}

export async function deleteQuiz(quizId: string): Promise<void> {
  return apiClient.delete(`/quizzes/${quizId}`);
}
