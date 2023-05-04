from .entities.entity import Session, engine, Base
from .entities.question import Question

# generate database schema
Base.metadata.create_all(engine)

# start session
session = Session()

# check for existing data
questions = session.query(Question).all()

if len(questions) == 0:
    # create and persist mock questions
    python_question = Question("SQLAlchemy Question", "Test your knowledge about SQLAlchemy.", "script")
    session.add(python_question)
    session.commit()
    session.close()

    # reload questions
    questions = session.query(Question).all()

# show existing questions
print('### questions:')
for question in questions:
    print(f'({question.id}) {question.text_question}')