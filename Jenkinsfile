pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = 'dockerhub-mohamedaf288'
        BACKEND_IMAGE = 'react-mongo-flask-main-backend:latest'
        FRONTEND_IMAGE = 'react-mongo-flask-main-frontend:latest'
    }

    stages {
        stage('Build Backend') {
            steps {
                sh 'docker build -t $BACKEND_IMAGE ./backend'
            }
        }

        stage('Build Frontend') {
            steps {
                sh 'docker build -t $FRONTEND_IMAGE ./frontend'
            }
        }

        stage('Push Images') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: DOCKERHUB_CREDENTIALS,
                        usernameVariable: 'USER',
                        passwordVariable: 'PASS'
                    )
                ]) {
                    sh '''
                        echo "$PASS" | docker login -u "$USER" --password-stdin
                        docker push $BACKEND_IMAGE
                        docker push $FRONTEND_IMAGE
                    '''
                }
            }
        }

        stage('Finish') {
            steps {
                echo "🎉 All builds and deployments completed successfully!"
            }
        }
    }

    post {
        always {
            echo "Containers currently running on this machine:"
            sh 'docker ps'
        }
    }
}
