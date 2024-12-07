export interface Quiz {
  id: string,
  name: string,
  description: string,
  created_at: string,
  updated_at: string,
  creator: {},
  questions: Question[],
}

export interface Question {
  id?: number;
  question: string;
  answers: Answer[];
  answeringTimeInSeconds: number;
}

export interface Answer {
  id?: number;
  text: string;
  correct: boolean;
}
