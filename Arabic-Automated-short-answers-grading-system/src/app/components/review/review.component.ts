import { Component } from '@angular/core';
import { AnswerService } from '../question-section/answer-service';
import { GradeService } from '../question-section/grade-service';
import { QuestionService } from '../question-section/question-service';
import { ActivatedRoute } from '@angular/router';
import { Answer } from '../interfaces/answer';
import { Grade } from '../interfaces/grade';
import { Question } from '../interfaces/question';

@Component({
  selector: 'app-review',
  templateUrl: './review.component.html',
  styleUrls: ['./review.component.css']
})
export class ReviewComponent {

  answers: Answer[] = [];
  grades: Grade[] = [];
  questions: Question[] = [];
  totalScore = 0;
  
  constructor(
    private answerService: AnswerService,
    private gradeService: GradeService,
    private questionService: QuestionService,
    private route: ActivatedRoute
  ) { }
  ngOnInit(): void {
    this.fetchAnswers();
    this.fetchQuestions();
    //this.fetchGrades();
  }
  fetchAnswers() {
    this.answerService.fetchAnswers()
      .subscribe(answers => {
        this.answers = answers;
        this.fetchGrades();
      });
  }
  fetchQuestions() {
    this.questionService.fetchQuestions()
      .subscribe(questions => this.questions = questions);
  }
  fetchGrades() {
    this.gradeService.fetchGrades()
      .subscribe(grades => {
        this.grades = grades;
        this.calculateScore();
      });
  }
  calculateScore(): void {
    this.totalScore = this.grades.reduce((total, grade) => total + grade.score, 0);
  }
  getQuestionText(questionId: number): string {
    return this.questions.find(question => question.id === questionId)?.text_question || '';
  }

  getAnswerText(answerId: number): string {
    return this.answers.find(answer => answer.answerId === answerId)?.text_answer || '';
  }
  
}
