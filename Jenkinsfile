pipeline {
    agent any
    stages {
        stage('Clone Repository') {
            steps {
                git 'https://github.com/votre-repo/ml_app.git'
            }
        }
        stage('Install Dependencies') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }
        stage('Run Tests') {
            steps {
                sh 'pytest tests/'
            }
        }
        stage('Train Model') {
            steps {
                sh 'python app/model_training.py'
            }
        }
        stage('Push Model to DVC') {
            steps {
                sh 'dvc push'
            }
        }
    }
}
