pipeline {
    agent any

    environment {
        DATA_FILE = 'data\\processed\\data.csv' // Chemin Windows avec double antislash
        PYTHON_HOME = 'C:\\Python39'  // Chemin vers ton installation Python (à adapter)
        PATH = "${PYTHON_HOME}\\Scripts;${PYTHON_HOME};${env.PATH}" // Ajouter Python et Scripts à PATH
    }

    stages {
        stage('Check and Install pip') {
            steps {
                script {
                    // Vérifier si pip est installé
                    def pipCheck = bat(script: 'pip --version', returnStatus: true)
                    if (pipCheck != 0) {
                        // Si pip n'est pas installé, l'installer
                        echo 'pip n\'est pas installé, installation en cours...'
                        bat 'python -m ensurepip --upgrade'
                        bat 'python -m pip install --upgrade pip'
                    } else {
                        echo 'pip est déjà installé.'
                    }
                }
            }
        }

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
