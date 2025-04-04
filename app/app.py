from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
import os
import joblib

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

# Répertoire pour sauvegarder les modèles
MODEL_SAVE_DIR = 'models/'

# Créer le répertoire si il n'existe pas
if not os.path.exists(MODEL_SAVE_DIR):
    os.makedirs(MODEL_SAVE_DIR)

# --------------------------------------------
# DEBUT VISUALISATION - FALL OUSSEYNOU
# --------------------------------------------

# @app.route('/visualisation')
# def visualisation():
#     models = MLModel.query.all()
#
#     if models:
#         # 📊 Graphique 1 : Afficher la précision des modèles entraînés
#         plt.figure(figsize=(8, 5))
#         model_names = [model.model_type for model in models]
#         accuracies = [model.accuracy for model in models]
#
#         sns.barplot(x=model_names, y=accuracies, palette="viridis")
#         plt.title("Précision des modèles entraînés")
#         plt.xlabel("Modèle")
#         plt.ylabel("Précision (%)")
#
#         # Sauvegarde de l'image dans un dossier static
#         graph_path = "static/images/model_accuracy.png"
#         plt.savefig(graph_path)
#         plt.close()
#
#         return render_template('visualisation.html', graph_path=graph_path, models=models)
#
#     else:
#         return "Aucun modèle n'a encore été entraîné."

@app.route('/visualisation')
def visualisation():
    models = MLModel.query.all()

    if models:
        # Filtrer les modèles dont la précision est nulle
        valid_models = [model for model in models if model.accuracy is not None]

        if not valid_models:
            return "Aucun modèle de classification n'a été entraîné (précision non applicable)."

        # Extraire des données pour le plotting
        model_names = [model.model_type for model in valid_models]
        accuracies = [float(model.accuracy) for model in valid_models]  # Ensure numeric type

        # Créez un répertoire static/images si nécessaire
        image_dir = os.path.join(app.static_folder, 'images')
        os.makedirs(image_dir, exist_ok=True)

        # Generate the plot
        plt.figure(figsize=(8, 5))
        sns.barplot(x=model_names, y=accuracies, palette="viridis")
        plt.title("Précision des modèles entraînés (Classification)")
        plt.xlabel("Modèle")
        plt.ylabel("Précision (%)")

        # Save the plot
        graph_file = 'model_accuracy.png'
        full_path = os.path.join(image_dir, graph_file)
        plt.savefig(full_path)
        plt.close()

        graph_path = os.path.join('images', graph_file)
        return render_template('visualisation.html', graph_path=graph_path, models=models)

    else:
        return "Aucun modèle n'a encore été entraîné."

# --------------------------------------------
# FIN VISUALISATION - OUSSEYNOU
# --------------------------------------------


# --------------------------------------------
# DEBUT MODEL MACHINE LEARNING - HERMAN
# --------------------------------------------

class MLModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(200), nullable=False)
    model_type = db.Column(db.String(50), nullable=False)
    accuracy = db.Column(db.Float, nullable=True)
    model_path = db.Column(db.String(200), nullable=False)  # Chemin du modèle sauvegardé
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'Model {self.model_type} - Accuracy: {self.accuracy}%'
    
@app.route('/train', methods=['POST', 'GET'])
def train_model():
    if request.method == 'POST':
        file_path = request.form['file_path']
        model_type = request.form['model_type']
        
        # Charger les données
        data = pd.read_csv(file_path)

        # Vérifier si la colonne 'date' existe et la convertir
        if 'date' in data.columns:
            data['date'] = pd.to_datetime(data['date'], errors='coerce')  # Convertir en datetime
            data['date'] = data['date'].astype(int) / 10**9  # Convertir en timestamp
        
        # Séparer les features et la cible
        X = data.iloc[:, :-1]  # On garde les features
        y = data.iloc[:, -1]  # On garde la cible (dernier colonne)

        # Encodage des variables catégoriques dans X
        label_encoders = {}  # Stocker les encodeurs pour plus tard
        for col in X.columns:
            if X[col].dtype == 'object':  # Vérifier si c'est une colonne textuelle
                le = LabelEncoder()
                X[col] = le.fit_transform(X[col])
                label_encoders[col] = le  # Sauvegarde de l'encodeur

        # Encodage de la colonne cible (y) si c'est une catégorie (ex: 'Iris-setosa')
        if y.dtype == 'object':
            y_encoder = LabelEncoder()
            y = y_encoder.fit_transform(y)  # Convertir les classes en nombres
        else:
            y_encoder = None

        # Diviser les données en train/test
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Convertir en `numpy.ndarray`
        X_train = X_train.values
        X_test = X_test.values

        # Choisir le modèle
        if model_type == 'Linear Regression':
            model = LinearRegression()
        elif model_type == 'SVM':
            model = SVC()

        # Entraîner le modèle
        model.fit(X_train, y_train)

        # Prédictions et évaluation
        y_pred = model.predict(X_test)

        # Calculer la précision (uniquement pour classification)
        accuracy = accuracy_score(y_test, y_pred) * 100 if model_type == 'SVM' else None

        # Sauvegarder le modèle avec joblib
        model_filename = f"{model_type.replace(' ', '_').lower()}_model.pkl"
        model_path = os.path.join(MODEL_SAVE_DIR, model_filename)
        joblib.dump(model, model_path)

        # Sauvegarde dans la base de données
        new_model = MLModel(file_name=file_path, model_type=model_type, accuracy=accuracy, model_path=model_path)
        db.session.add(new_model)
        db.session.commit()

        # return f"Acuracy : {accuracy}"
        return redirect(url_for('visualisation'))

    return render_template('train_model.html')
    
# --------------------------------------------
# FIN MODEL MACHINE LEARNING - HERMAN
# --------------------------------------------
    
with app.app_context():
    db.create_all()


# --------------------------------------------
# DEBUT BACKEND API - NDIAGA BEYE
# --------------------------------------------

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    
    if file.filename == '':
        return 'No selected file'
    
    # Sauvegarder le fichier dans le répertoire
    file_path = os.path.join('uploads', file.filename)
    file.save(file_path)

    # Lire le fichier CSV dans un DataFrame
    data = pd.read_csv(file_path)

    # Affichage des premières lignes du fichier téléchargé
    print(data.head())

    return redirect(url_for('train_model', file_path=file_path))

# --------------------------------------------
# FIN BACKEND API - NDIAGA BEYE
# --------------------------------------------

if __name__ == "__main__":
    app.run(debug=True)

#FIN BACKEND API - NDIAGA BEYE