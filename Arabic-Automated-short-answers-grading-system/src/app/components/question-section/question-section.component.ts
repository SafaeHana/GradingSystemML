import { Component, OnInit } from '@angular/core';

import { QuestionService } from './question-service';
import { AnswerService } from './answer-service';
import { Answer } from '../interfaces/answer';




@Component({
  selector: 'app-question-section',
  templateUrl: './question-section.component.html',
  styleUrls: ['./question-section.component.css']
})
export class QuestionSectionComponent {

  isTestVisible = false;   // Test Visibility
  isInstructionsVisible = true;  // Instructions Visibility
  currentQuestionIndex = 0;  
  isFinished=false; // // finished test Visibility
  currentQuestion: any; // or define a more specific type for the questions array
  currentAnswer: Answer = {answerId:0, questionId: 0, text_answer: '' };
  questions: any =  [
    { id: 1,
    text: 'ffffffffffffffff',
   
    },
    {  id: 2,
      text: 'jjjjjjjjjjjj',
    },
    {
      id: 3,
      text: 'mmmmmmmmmmmmmmmmmmmmmmm',
    }
    ];
  constructor(private questionService: QuestionService, private answerService: AnswerService) { }

  ngOnInit(): void { //It is typically used to perform any initialization that is required for the component, such as initializing properties, calling services to retrieve data, or setting up event listeners.
    this.fetchQuestions();
    this.currentQuestion = this.questions[0];
  }
  

  startQuiz() {
    this.isTestVisible = true;
    this.isInstructionsVisible =false;
    this.isFinished = false;
  }

  fetchQuestions(): void {
    this.questionService.fetchQuestions()
      .subscribe(questions => {
        this.questions = this.questions;
        this.currentQuestion = this.questions[this.currentQuestionIndex];
        this.currentAnswer.questionId = this.currentQuestion.id;

      });
  }

  submitAnswer(): void {
    this.answerService.submitAnswers([this.currentAnswer])
    // Storing in database the answers
      .subscribe(() => {
        
        if (this.currentQuestionIndex < this.questions.length-1) {
          this.currentQuestionIndex++;
          this.currentQuestion = this.questions[this.currentQuestionIndex];
          this.currentAnswer = { answerId:this.currentQuestion.id ,questionId: this.currentQuestion.id, text_answer: '' };
        } else {
          console.log('All answers submitted!');
          this.isTestVisible = false;

        }
      });
      
    //Next button traitement 
    if (this.currentQuestionIndex <this.questions.length-1) {
      this.currentQuestionIndex++;
      this.currentQuestion = this.questions[this.currentQuestionIndex];
      this.currentAnswer = { answerId:this.currentQuestion.id ,questionId: this.currentQuestion.id, text_answer: '' };
      this.currentAnswer.text_answer = ''; // clear the answer textarea

    } else {
      console.log('No more questions!');
      this.isTestVisible = false;
      this.isFinished = true;
    }
  }
  // Show Scores of each answer and total score 
  finishTest() {
    throw new Error('Method not implemented.');
    }
  }

