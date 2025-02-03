pipeline {
    agent { 
        dockerfile true 
    }

    stages {
        stage('Build') {
            steps {
                script {
                    echo 'Jenkins build triggered by GitHub webhook.'
                }
            }
        }
    }
}