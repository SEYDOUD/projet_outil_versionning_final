pipeline {
    agent any

    environment {
        DATA_FILE = 'data\\processed\\data.csv' // Chemin Windows avec double antislash
    }

    stages {
        stage('Inject GDrive Secrets') {
            steps {
                withCredentials([
                    string(credentialsId: 'GDRIVE_CLIENT_ID', variable: 'GDRIVE_CLIENT_ID'),
                    string(credentialsId: 'GDRIVE_CLIENT_SECRET', variable: 'GDRIVE_CLIENT_SECRET')
                ]) {
                    bat 'echo Client ID: %GDRIVE_CLIENT_ID%'
                    bat 'echo Client Secret: %GDRIVE_CLIENT_SECRET%'

                    // Écrire les valeurs dans un fichier de config DVC
                    bat '''
                    echo [remote "gdrive"] > .dvc\\config.local
                    echo     client_id = %GDRIVE_CLIENT_ID% >> .dvc\\config.local
                    echo     client_secret = %GDRIVE_CLIENT_SECRET% >> .dvc\\config.local
                    '''
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
