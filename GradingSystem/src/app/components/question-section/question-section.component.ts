import { Component, OnInit } from '@angular/core';
import {Router} from "@angular/router";

import { QuestionService } from '../../services/question-service';
import { AnswerService } from '../../services/answer-service';
import { Answer } from '../../models/answer.model';
import { Question } from '../../models/question.model';




@Component({
  selector: 'app-question-section',
  templateUrl: './question-section.component.html',
  styleUrls: ['./question-section.component.css']
})
export class QuestionSectionComponent {
// Initialize the current maximum ID to 0
  currentMaxId = 0;
  isTestVisible = false;   // Test Visibility
  isInstructionsVisible = true;  // Instructions Visibility
  currentQuestionIndex = 0;  
  isFinished=false; // // finished test Visibility
  currentQuestion: any; // or define a more specific type for the questions array
  currentAnswer: Answer = {text_answer: '', question_id: 0, student_id:0 };
  questions!: Question[];
  constructor(private questionService: QuestionService, private answerService: AnswerService, private router: Router) { }

  ngOnInit(): void { //It is typically used to perform any initialization that is required for the component, such as initializing properties, calling services to retrieve data, or setting up event listeners.
    this.fetchQuestions();
    //this.currentQuestion = this.questions[0];
  }
  

  startQuiz() {
    this.isTestVisible = true;
    this.isInstructionsVisible =false;
    this.isFinished = false;
  }

  fetchQuestions(): void {
    this.questionService.fetchQuestions().subscribe(questions => {
      this.questions = questions;
      this.currentQuestion = this.questions[this.currentQuestionIndex];
      this.currentAnswer.question_id = this.currentQuestion.id;
    });
  }
 
  
  
  
  
  submitAnswer(): void {
   
    // Update the current answer with the next question's ID and student ID
    this.currentAnswer.question_id = this.currentQuestion.id;
    this.currentAnswer.student_id = 1;
     // Set the text_answer to the current value of the textarea
    this.currentAnswer.text_answer = this.currentAnswer.text_answer.trim();

  
    // Submit the current answer to the server
    this.answerService.submitAnswers(this.currentAnswer).subscribe(response => {
      console.log('Answer saved successfully:', response);
      console.log(this.currentAnswer);
      if (this.currentQuestionIndex < this.questions.length - 1) {
        // If there are more questions, move to the next question
        this.currentQuestionIndex++;
        this.currentQuestion = this.questions[this.currentQuestionIndex];
        this.currentAnswer = {
        // id: ++this.currentMaxId,
          text_answer: '',
          question_id: this.currentQuestion.id,
          student_id: this.currentQuestion.id
        };
      } else {
        // If there are no more questions, hide the test section
        console.log('All answers submitted!');
        this.isTestVisible = false;
        this.isFinished = true;

      }
    }, error => {
      console.log('Error submitting answer:', error);
    });
  }
  
  }

