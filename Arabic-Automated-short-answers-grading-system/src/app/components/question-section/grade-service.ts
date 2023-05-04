import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Grade } from '../interfaces/grade';
import { API_URL } from 'src/env';

@Injectable({
  providedIn: 'root'
})
export class GradeService {
  private fetchGradesUrl =  `${API_URL}/fetchGrades`; // safae dont forget to modify URL to match your backend API
 
  constructor(private http: HttpClient) { }

 
  fetchGrades(): Observable<Grade[]> {
    return this.http.get<Grade[]>(this.fetchGradesUrl);
  }
}