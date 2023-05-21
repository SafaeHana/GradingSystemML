# Système automatisé de notation de réponses courtes en arabe pour l'histoire marocaine
## Description du projet
Le projet consiste à développer un système automatisé de notation de réponses courtes en arabe pour l'histoire marocaine. L'objectif de ce système est de donner une note adéquate aux étudiants en fonction de leurs réponses. Le système doit être en arabe et nous allons préparer notre propre ensemble de données.
### Le projet sera réalisé en suivant les étapes suivantes :

- Scraping des données à partir de différentes sources : sites web arabes, ensembles de données, livres, etc.
- Mise en place d'un pipeline de traitement du langage naturel en arabe.
- Word embedding et encodage des mots.
- Entraînement du modèle basé sur des algorithmes d'apprentissage automatique classiques.
- Évaluation des modèles et choix du meilleur modèle.
- Déploiement du modèle et intégration dans une application web SPA (Single Page Application).

## Prérequis
Avant de commencer, assurez-vous d'avoir les éléments suivants installés :
- Python 
- Flask 
- SQLAlchemy 
- MYSQL
## Installation
#### Clonez le dépôt du projet depuis GitHub :
git clone https://github.com/votre-utilisateur/nom-du-projet.git
#### Accédez au répertoire du projet :
cd nom-du-projet
#### Créez un environnement virtuel :
python -m venv myvenv
#### Activez l'environnement virtuel :
- Sous Windows :
myvenv\Scripts\activate
- Sous macOS/Linux :
source myvenv/bin/activate
#### Installez les dépendances du projet :
pip install -r requirements.txt
#### Configurez la base de données MYSQL :
Créez une nouvelle base de données nommée "online_exam".
Modifiez le fichier de configuration entity.py avec les informations de votre base de données.
### Utilisation
Lancez l'application Flask :
flask run
Accédez à l'URL suivante dans votre navigateur :
http://localhost:5000
Vous pouvez maintenant utiliser l'application pour créer de nouvelles instances d'examens et visualiser les résultats.
Structure du projet
### Contributions
Safae Mazozi & Ouidad Oualhaj 
made with love 
