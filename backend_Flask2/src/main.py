# coding=utf-8
from flask import Flask, jsonify, request
from flask_cors import CORS
from .entities.entity import Session, engine, Base
from .entities.question import Question, QuestionSchema
from .entities.answer import Answer, AnswerSchema
from .entities.grade import Grade
from .entities.grade import GradeSchema

from sklearn.model_selection import train_test_split
import pickle
import nltk
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd 
import seaborn as sns
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem import PorterStemmer
from gensim.models import Word2Vec
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd 
import seaborn as sns
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import cosine_distances
import warnings 
warnings.filterwarnings('ignore')



#--------------------------------------------ML Code -------------------------------------------
# apload data
df2 = pd.read_csv("C:/Users/safae/Documents/lsIS4/ML2/Dataset_Small_range.csv")
df1 = pd.read_csv("C:/Users/safae/Documents/lsIS4/ML2/new_DATASET1 (1).csv")

# Fusionner les deux ensembles de données en utilisant la colonne commune : Question_id
df = pd.merge(df1, df2, on='Question_id')
df.head()
#Tokenisation
df['Answers'] = df['Answers'].apply(nltk.word_tokenize)

#Drop stop words
stop_words = set(stopwords.words('Arabic'))
df['Answers'] = df['Answers'].apply(lambda x: [w for w in x if not w in stop_words])

#Lemmatization & stemming
stemmer = PorterStemmer()
# Stem words in answers column
df['Answers'] = df['Answers'].apply(lambda x: [stemmer.stem(word) for word in x])

lemmatizer = WordNetLemmatizer()
# Lemmatize words in answers column
df['Answers'] = df['Answers'].apply(lambda x: [lemmatizer.lemmatize(word) for word in x])

#df.head()
#Word2Vec
model = Word2Vec(df['Answers'], min_count=1)
#Vectorise toutes les réponses:::
max_len = model.vector_size

W = np.zeros((len(df['Answers']), max_len))
for i, sentence in enumerate(df['Answers']):
    word_vectors = []
    for word in sentence:
        if word in model.wv:
            word_vectors.append(model.wv[word])
    if len(word_vectors) > 0:
        mean_vector = np.mean(word_vectors, axis=0)
        W[i, :] = mean_vector



#Vectorise la réponse d'etudiant
def verctoriseResponse(response):
    # Tokeniser la réponse entrée
    response_tokens = nltk.word_tokenize(response)
    
    # Supprimer les mots d'arrêt de la réponse
    response_tokens = [w for w in response_tokens if not w in stop_words]
    
    # Appliquer le stemming à la réponse
    response_tokens = [stemmer.stem(word) for word in response_tokens]
    
    # Appliquer la lemmatisation à la réponse
    response_tokens = [lemmatizer.lemmatize(word) for word in response_tokens]
    
    # Vectoriser la réponse en utilisant le modèle Word2Vec
    response_vector = np.mean([model.wv[word] for word in response_tokens if word in model.wv], axis=0)
    
    return response_vector

def find_existing_answers_vectors(df, question_id, W):

    if question_id in df['Question_id'].values:
        # Trouver tous les indices correspondants à l'ID de la question
        question_indices = df.index[df['Question_id'] == question_id].tolist()

        # Extraire les vecteurs de réponse correspondants à partir de la matrice W
        existing_answers_vectors = []
        for i in question_indices:
            existing_answers_vectors.append(W[i])
    else:
        print("L'ID de la question que vous avez fourni est incorrect")
        existing_answers_vectors = None
    existing_answers_vectors = np.array(existing_answers_vectors)
    return existing_answers_vectors

# -------------------- Model : predicting the score : -------------------------------
def prediction(response_vector, existing_answers_vectors , question_id):
    from sklearn.ensemble import GradientBoostingRegressor
    
    #existing_answers_vectors = find_existing_answers_vectors(df, question_id, W)
    
    # Split the data into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(existing_answers_vectors, df[(df['Question_id'] == question_id)]['Score'], test_size=0.2, random_state=42)
    
    # Create and train the Gradient Boosted Regression model
    gb_model = GradientBoostingRegressor(n_estimators=100, random_state=42)
    gb_model.fit(X_train, y_train)
    
    # Reshape response vector to have shape (1, n)
    response_vector_reshaped = response_vector.reshape(1, -1)
    
    # Predict the score using the Gradient Boosted Regression model
    score_prediction = gb_model.predict(response_vector_reshaped)
    #print("Predicted score:", score_prediction[0])
    return score_prediction[0]



#------------------------------------- creating the Flask application----------------------------------------------
app = Flask(__name__)
# ... other import statements .
CORS(app)


# if needed, generate database schema
Base.metadata.create_all(engine)

#--------------------------------------------------questions-------------------------------------------------------------
#Les routes qui gérent les requetes et les reponses :
@app.route('/questions')
def fetchQuestions(): # recupérer les question depuis la db
    # fetching from the database
    session = Session()
    question_objects = session.query(Question).all()

    # transforming into JSON-serializable objects
    schema = QuestionSchema(many=True)
    questions = schema.dump(question_objects)

    # serializing as JSON
    session.close()
    return jsonify(questions)

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
    answers = schema.dump(Answer_objects)

    # serializing as JSON
    session.close()
    return jsonify(answers)


@app.route('/answers', methods=['POST'])
def submitAnswers():
    # mount answer object
    posted_answer = AnswerSchema(only=('text_answer', 'question_id', 'student_id')).load(request.get_json(), many=False)
    answer = Answer(**posted_answer)

    session = Session()
    session.add(answer)
    session.commit()
    #Calling  verctoriseResponse , find_existing_answers_vectors , prediction Functions
    # on vectorise la réponse 
    response_vector = verctoriseResponse(answer.text_answer)
    #on récupere toutes les réponses d'entrainement  qui ont le meme question_id 
    existing_answers_vectors = find_existing_answers_vectors(df,answer.question_id,W)
    # ici  le modele prend comme arguments le retour des deux fonction precedentes ,
    predicted_score = prediction(response_vector,existing_answers_vectors,answer.question_id)
    print("predicted score :", predicted_score)
    #Apres la prédiction du score , on l'stocker dans db on utilisant la fonction submitGrades
    submitGrades(score=predicted_score, answer_id=answer.id, student_id=answer.student_id)
    print("grades submitted")
    # return created answer
    answer_schema = AnswerSchema()
    response = answer_schema.dump(answer)
   
    session.close()
    return jsonify(response), 201

   
#--------------------------------------------------------grades----------------------------------------------------------------
# On a appelé cette fonction dans la fonction submitAnswer
def submitGrades(score, answer_id, student_id):
    # create a dictionary with the attribute values
    posted_grade = {
        'score': score,
        'answer_id': answer_id,
        'student_id': student_id
       
    }
    print()
    # mount grade object
    grade = Grade(**posted_grade)

    session = Session()
    try:
        session.add(grade)
        session.commit()
    except Exception as e:
        session.rollback()
        print("Error while adding grade to database:", str(e))
        return jsonify({"error": "Failed to add grade to database"}), 500

    # return created grade
    grade_schema = GradeSchema()
    response = grade_schema.dump(grade)
    session.close()
    return jsonify(response), 201

@app.route('/grades')
def fetchGrades():
    # fetching from the database
    session = Session()
    Grade_objects = session.query(Grade).all()

    # transforming into JSON-serializable objects
    schema = GradeSchema(many=True)
    grades = schema.dump(Grade_objects)

    # serializing as JSON
    session.close()
    return jsonify(grades)
#--------------------------------------------------Register-------------------------------------------------------------------
@app.route('/register', methods=['POST'])
def register():
    json_data = request.json
    user = User(
        email=json_data['email'],
        password=json_data['password']
    )
    try:
        db.session.add(user)
        db.session.commit()
        status = 'success'
    except:
        status = 'this user is already registered'
    db.session.close()






#C'est tous Merci 