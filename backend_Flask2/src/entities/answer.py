
from sqlalchemy import Column, String, ForeignKey, Integer
from marshmallow import Schema, fields
from .entity import Entity, Base
from sqlalchemy.orm import relationship
from . import question
from . import student


class AnswerSchema(Schema):
    id = fields.Number()
    text_answer = fields.Str()
    question_id= fields.Number()
    student_id=fields.Number()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    last_updated_by = fields.Str()
    
class Answer(Entity, Base):
    __tablename__ = 'answers'
    id = Column(Integer, primary_key=True)
    text_answer = Column(String(255))
    question_id = Column(Integer, ForeignKey('questions.id'))
    student_id = Column(Integer, ForeignKey('students.id'))

   

    def __init__(self, text_answer, created_by, question_id ,student_id):
        Entity.__init__(self, created_by)
        self.text_answer = text_answer
        self.question_id = question_id
        self.student_id = student_id

        
