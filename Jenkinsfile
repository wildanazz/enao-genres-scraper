pipeline {
    agent { dockerfile true }

    stages {
        stage('Docker Test') {
            steps {
                script {
                    sh 'docker --version'
                }
            }
        }
    }
}