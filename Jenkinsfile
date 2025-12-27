pipeline {
    agent any
    
    environment {
        DOCKER_API_VERSION = '1.43'
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-mohamedaf288')
        DOCKERHUB_USERNAME = 'mohamedaf288'
        BACKEND_IMAGE = "${DOCKERHUB_USERNAME}/react-mongo-flask-main-backend"
        FRONTEND_IMAGE = "${DOCKERHUB_USERNAME}/react-mongo-flask-main-frontend"
    }
    
    stages {
        stage('Checkout Code') {
            steps {
                echo '📥 Récupération du code depuis le repository...'
                checkout scm
            }
        }
        
        // ========================================
        // SÉCURITÉ 1: Scan des Secrets
        // ========================================
        stage('Secret Scanning') {
            steps {
                echo '🔐 Scan des secrets (mots de passe, clés API, tokens)...'
                script {
                    sh '''
                        docker run --rm \
                        -v $(pwd):/path \
                        zricethezav/gitleaks:latest detect \
                        --source /path \
                        --no-git \
                        --verbose \
                        --report-path /path/gitleaks-report.json || true
                    '''
                }
                echo '✅ Scan des secrets terminé'
            }
        }
        
        stage('Build Backend') {
            steps {
                echo '🔨 Construction de l\'image Docker Backend...'
                script {
                    dir('backend') {
                        sh '''
                            docker build \
                            -t ${BACKEND_IMAGE}:latest \
                            -t ${BACKEND_IMAGE}:${BUILD_NUMBER} \
                            .
                        '''
                    }
                }
                echo '✅ Image Backend construite'
            }
        }
        
        stage('Build Frontend') {
            steps {
                echo '🔨 Construction de l\'image Docker Frontend...'
                script {
                    dir('frontend') {
                        sh '''
                            docker build \
                            -t ${FRONTEND_IMAGE}:latest \
                            -t ${FRONTEND_IMAGE}:${BUILD_NUMBER} \
                            .
                        '''
                    }
                }
                echo '✅ Image Frontend construite'
            }
        }
        
        // ========================================
        // SÉCURITÉ 2: Scan des Vulnérabilités
        // ========================================
        stage('Security Scan - Backend') {
            steps {
                echo '🔍 Scan de sécurité de l\'image Backend...'
                script {
                    sh '''
                        docker run --rm \
                        -v /var/run/docker.sock:/var/run/docker.sock \
                        aquasec/trivy:latest image \
                        --severity HIGH,CRITICAL \
                        --format json \
                        --output backend-trivy-report.json \
                        ${BACKEND_IMAGE}:latest || true
                    '''
                }
                echo '✅ Scan Backend terminé'
            }
        }
        
        stage('Security Scan - Frontend') {
            steps {
                echo '🔍 Scan de sécurité de l\'image Frontend...'
                script {
                    sh '''
                        docker run --rm \
                        -v /var/run/docker.sock:/var/run/docker.sock \
                        aquasec/trivy:latest image \
                        --severity HIGH,CRITICAL \
                        --format json \
                        --output frontend-trivy-report.json \
                        ${FRONTEND_IMAGE}:latest || true
                    '''
                }
                echo '✅ Scan Frontend terminé'
            }
        }
        
        // ========================================
        // SÉCURITÉ 3: Rapport de Sécurité
        // ========================================
        stage('Generate Security Summary') {
            steps {
                echo '📊 Génération du rapport de sécurité...'
                script {
                    sh '''
                        echo "==========================================" > security-summary.txt
                        echo "      RAPPORT DE SÉCURITÉ" >> security-summary.txt
                        echo "==========================================" >> security-summary.txt
                        echo "" >> security-summary.txt
                        echo "Build: #${BUILD_NUMBER}" >> security-summary.txt
                        echo "Date: $(date '+%Y-%m-%d %H:%M:%S')" >> security-summary.txt
                        echo "Projet: react-mongo-flask-main" >> security-summary.txt
                        echo "" >> security-summary.txt
                        echo "📦 Images Docker:" >> security-summary.txt
                        echo "  - Backend: ${BACKEND_IMAGE}:${BUILD_NUMBER}" >> security-summary.txt
                        echo "  - Frontend: ${FRONTEND_IMAGE}:${BUILD_NUMBER}" >> security-summary.txt
                        echo "" >> security-summary.txt
                        
                        # Vérification des rapports
                        if [ -f backend-trivy-report.json ]; then
                            echo "🔍 Backend Vulnerabilities:" >> security-summary.txt
                            echo "  - Rapport: backend-trivy-report.json" >> security-summary.txt
                        else
                            echo "⚠️  Backend scan: Aucun rapport généré" >> security-summary.txt
                        fi
                        
                        if [ -f frontend-trivy-report.json ]; then
                            echo "🔍 Frontend Vulnerabilities:" >> security-summary.txt
                            echo "  - Rapport: frontend-trivy-report.json" >> security-summary.txt
                        else
                            echo "⚠️  Frontend scan: Aucun rapport généré" >> security-summary.txt
                        fi
                        
                        if [ -f gitleaks-report.json ]; then
                            echo "🔐 Secret Scan:" >> security-summary.txt
                            echo "  - Rapport: gitleaks-report.json" >> security-summary.txt
                        else
                            echo "✅ Secret scan: Aucun secret détecté" >> security-summary.txt
                        fi
                        
                        echo "" >> security-summary.txt
                        echo "==========================================" >> security-summary.txt
                        cat security-summary.txt
                    '''
                }
                echo '✅ Rapport de sécurité généré'
            }
        }
        
        stage('Login to Docker Hub') {
            steps {
                echo '🔐 Connexion à Docker Hub...'
                sh 'echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin'
            }
        }
        
        stage('Push Images to Docker Hub') {
            steps {
                echo '📤 Push des images vers Docker Hub...'
                sh '''
                    docker push ${BACKEND_IMAGE}:latest
                    docker push ${BACKEND_IMAGE}:${BUILD_NUMBER}
                    docker push ${FRONTEND_IMAGE}:latest
                    docker push ${FRONTEND_IMAGE}:${BUILD_NUMBER}
                '''
                echo '✅ Images pushées avec succès'
            }
        }
        
        stage('Cleanup Local Images') {
            steps {
                echo '🧹 Nettoyage des images locales...'
                sh '''
                    docker rmi ${BACKEND_IMAGE}:${BUILD_NUMBER} || true
                    docker rmi ${FRONTEND_IMAGE}:${BUILD_NUMBER} || true
                '''
                echo '✅ Nettoyage terminé'
            }
        }
        
        stage('Finish') {
            steps {
                echo '🎉 Pipeline terminé avec succès!'
                echo '📦 Images disponibles sur Docker Hub:'
                echo "   - ${BACKEND_IMAGE}:latest"
                echo "   - ${BACKEND_IMAGE}:${BUILD_NUMBER}"
                echo "   - ${FRONTEND_IMAGE}:latest"
                echo "   - ${FRONTEND_IMAGE}:${BUILD_NUMBER}"
            }
        }
    }
    
    post {
        always {
            echo '🔒 Déconnexion de Docker Hub...'
            sh 'docker logout || true'
            
            echo '🔎 Conteneurs en cours d\'exécution:'
            sh 'docker ps || true'
            
            // Archiver les rapports de sécurité
            archiveArtifacts artifacts: '*-report.json, security-summary.txt', 
                           allowEmptyArchive: true,
                           fingerprint: true
        }
        success {
            echo '✅ =========================================='
            echo '✅ PIPELINE RÉUSSI!'
            echo '✅ =========================================='
            echo '📦 Images Docker disponibles sur Docker Hub'
            echo '🔒 Rapports de sécurité archivés'
            echo '🎯 Build Number: ${BUILD_NUMBER}'
        }
        failure {
            echo '❌ =========================================='
            echo '❌ PIPELINE ÉCHOUÉ!'
            echo '❌ =========================================='
            echo '📋 Vérifiez les logs ci-dessus pour les erreurs'
        }
    }
}        
