# coding=utf-8

from flask import Flask, jsonify, request
from flask_cors import CORS
from .entities.entity import Session, engine, Base
from .entities.question import Question, QuestionSchema
from .entities.answer import Answer, AnswerSchema

# creating the Flask application
app = Flask(__name__)

# ... other import statements ..
CORS(app)

# if needed, generate database schema
Base.metadata.create_all(engine)

#--------------------------------------------------questions-------------------------------------------------------------
@app.route('/questions')
def fetchQuestions():
    # fetching from the database
    session = Session()
    question_objects = session.query(Question).all()

    # transforming into JSON-serializable objects
    schema = QuestionSchema(many=True)
    questions = schema.dump(question_objects)

    # serializing as JSON
    session.close()
    return jsonify(questions.data)
@app.route('/questions', methods=['POST'])
def submitQuestions():
    # mount Question object
    posted_question = QuestionSchema(only=('text_question'))\
        .load(request.get_json())

    question = Question(**posted_question.data, created_by="HTTP post request")

    # persist question
    session = Session()
    session.add(question)
    session.commit()

    # return created question
    new_question = QuestionSchema().dump(question).data
    session.close()
    return jsonify(new_question), 201
#-----------------------------------------------------Answers------------------------------------------------------------
@app.route('/answers')
def fetchAnswers():
    # fetching from the database
    session = Session()
    Answer_objects = session.query(Answer).all()

    # transforming into JSON-serializable objects
    schema = AnswerSchema(many=True)
    answers = schema.dump(answer_objects)

    # serializing as JSON
    session.close()
    return jsonify(answers.data)


@app.route('/answers', methods=['POST'])
def submitAnswers():
    # mount answer object
    posted_answer = AnswerSchema(only=('text_answer', 'question_id'))\
        .load(request.get_json())

    answer = Answer(**posted_answer.data, created_by="HTTP post request")

    # persist answer
    session = Session()
    session.add(answer)
    session.commit()

    # return created answer
    new_answer = AnswerSchema().dump(answer).data
    session.close()
    return jsonify(new_answer), 201
#--------------------------------------------------------grades----------------------------------------------------------------
def fetchGrades():
    # fetching from the database
    session = Session()
    Grade_objects = session.query(Grade).all()

    # transforming into JSON-serializable objects
    schema = GradeSchema(many=True)
    grades = schema.dump(grade_objects)

    # serializing as JSON
    session.close()
    return jsonify(grades.data)