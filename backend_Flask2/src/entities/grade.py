
from sqlalchemy import Column, String, ForeignKey, Integer
from marshmallow import Schema, fields
from .entity import Entity, Base
from sqlalchemy.orm import relationship
from . import question
from . import student






class Grade(Entity, Base):
    __tablename__ = 'grades'
    id = Column(Integer, primary_key=True)
    question_id = Column(Integer, ForeignKey('questions.id'))
    student_id = Column(Integer, ForeignKey('students.id'))
    score = Column(Integer)

    def __init__(self, score, created_by, question_id, student_id):
        Entity.__init__(self, created_by)
        self.score = score
        self.question_id = question_id
        self.student_id= student_id

class GradeSchema(Schema):
    id = fields.Number()
    student_id= fields.Number()
    score=fields.Number()
    question_id=fields.Number()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    last_updated_by = fields.Str()