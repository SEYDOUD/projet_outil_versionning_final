pipeline {
    agent any

    environment {
        DATA_FILE = 'data\\processed\\data.csv' // Chemin Windows avec double antislash
    }

    stages {
        stage('Clone Repository') {
            steps {
                git branch: 'main', url: 'https://github.com/SEYDOUD/projet_outil_versionning_final.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                bat 'pip install -r requirements.txt'
                bat 'pip install dvc'
            }
        }

        stage('DVC Add') {
            steps {
                bat '''
                dvc add uploads/IRIS.csv
                dvc push
                '''
            }
        }

        stage('Push Model to DVC') {
            steps {
                bat 'dvc push'
            }
        }
    }

    post {
        success {
            echo '✅ Pipeline exécuté avec succès'
        }
        failure {
            echo '❌ Une erreur est survenue pendant l’exécution du pipeline'
        }
    }
}
