import numpy as np
import matplotlib.pyplot as plt
import pandas as pd 
import seaborn as sns
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import cosine_distances
import warnings 
warnings.filterwarnings('ignore')
import pickle

# apload data
df2 = pd.read_csv("Dataset_Small_range.csv")
df1 = pd.read_csv("new_DATASET1 (1).csv")

# Fusionner les deux ensembles de données en utilisant la colonne commune : Question_id
df = pd.merge(df1, df2, on='Question_id')
df.head()

import nltk
from nltk.tokenize import word_tokenize
#Tokenisation
df['Answers'] = df['Answers'].apply(nltk.word_tokenize)

#Drop stop words
from nltk.corpus import stopwords
stop_words = set(stopwords.words('Arabic'))
df['Answers'] = df['Answers'].apply(lambda x: [w for w in x if not w in stop_words])

#Lemmatization & stemming
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem import PorterStemmer

stemmer = PorterStemmer()
# Stem words in answers column
df['Answers'] = df['Answers'].apply(lambda x: [stemmer.stem(word) for word in x])

lemmatizer = WordNetLemmatizer()
# Lemmatize words in answers column
df['Answers'] = df['Answers'].apply(lambda x: [lemmatizer.lemmatize(word) for word in x])

#df.head()
#Word2Vec
from gensim.models import Word2Vec
model = Word2Vec(df['Answers'], min_count=1)
#Vectorise toutes les réponses
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
def prediction(response_vector, existing_answers_vectors):
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
    print("Predicted score:", score_prediction[0])
    return score_prediction