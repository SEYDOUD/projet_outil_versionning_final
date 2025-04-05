pipeline {
    agent any
    stages {
        stage('Clone Repository') {
            steps {
                git 'https://github.com/SEYDOUD/projet_outil_versionning_final'
            }
        }

        stage('Push Data to DVC') {
            steps {
                sh 'dvc add uploads/IRIS.csv'
            },
            steps {
                sh 'dvc push'
            }
        }
    }
}
