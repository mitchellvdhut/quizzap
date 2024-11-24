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
