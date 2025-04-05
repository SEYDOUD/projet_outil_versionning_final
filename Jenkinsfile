pipeline {
    agent any

    environment {
        DATA_FILE = 'data\\processed\\data.csv' // Chemin Windows avec double antislash
    }
    
       stages {
        stage('Inject GDrive Secrets') {
            steps {
                withCredentials([
                    string(credentialsId: 'GDRIVE_CLIENT_ID', '760292635713-ag06l6fh6rdq35tv6lgc2n2isvet511p.apps.googleusercontent.com'),
                    string(credentialsId: 'GDRIVE_CLIENT_SECRET', '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')
                ]) {
                    bat 'echo Client ID: %GDRIVE_CLIENT_ID%'
                    bat 'echo Client Secret: %GDRIVE_CLIENT_SECRET%'
                    
                    // Tu peux aussi écrire ces valeurs dans un fichier de conf utilisé par DVC
                    bat '''
                    echo [remote "gdrive"] > .dvc/config.local
                    echo \tclient_id = %GDRIVE_CLIENT_ID% >> .dvc/config.local
                    echo \tclient_secret = %GDRIVE_CLIENT_SECRET% >> .dvc/config.local
                    '''
                }
            }
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
