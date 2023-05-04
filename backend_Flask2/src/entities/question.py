# coding=utf-8

from sqlalchemy import Column, String, ForeignKey, Integer

from .entity import Entity, Base
from sqlalchemy.orm import relationship


class Question(Entity, Base):
    __tablename__ = 'questions'
    text_question = Column(String(255))
    answers = relationship("Answer", backref="question")
    grades = relationship("Grade", backref="question")

    def __init__(self, text_question, created_by):
        Entity.__init__(self, created_by)
        self.text_question = text_question


class Answer(Entity, Base):
    __tablename__ = 'answers'
    id = Column(Integer, primary_key=True)
    text_answer = Column(String(255))
    question_id = Column(Integer, ForeignKey('questions.id'))

    def __init__(self, text_answer, created_by, question_id):
        Entity.__init__(self, created_by)
        self.text_answer = text_answer
        self.question_id = question_id


class Grade(Entity, Base):
    __tablename__ = 'grades'
    id = Column(Integer, primary_key=True)
    answer_id = Column(Integer, ForeignKey('questions.id'))
    score = Column(Integer)
