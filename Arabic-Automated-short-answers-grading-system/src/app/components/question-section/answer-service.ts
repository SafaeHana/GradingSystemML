import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Answer } from '../interfaces/answer';

@Injectable({
  providedIn: 'root'
})
export class AnswerService {
  private submitAnswersUrl = 'api/submitAnswers'; // safae dont forget to modify URL to match your backend API
  private fetchAnswersUrl = 'api/fetchAnswers'; // safae dont forget to modify URL to match your backend API

  constructor(private http: HttpClient) { }

  submitAnswers(answers: Answer[]): Observable<any> {
    return this.http.post<any>(this.submitAnswersUrl, answers);
  }
  fetchAnswers(): Observable<Answer[]> {
    return this.http.get<Answer[]>(this.fetchAnswersUrl);
  }
}