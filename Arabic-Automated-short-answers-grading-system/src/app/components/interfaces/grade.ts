export interface Grade {
    gradeId : number;
    score : number;
    questionId :number; // forign key
    answerId : number ; //forign key
}