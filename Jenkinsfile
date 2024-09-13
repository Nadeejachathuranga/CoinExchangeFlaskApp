pipeline {
    agent any
    
    stages { 
        stage('SCM Checkout') {
            steps {
                retry(3) {
                    git branch: 'main', url: 'https://github.com/Nadeejachathuranga/CoinExchangeFlaskApp'
                }
            }
        }
        stage('Build Docker Image') {
            steps {  
                bat 'docker build -t nadeejachathuranga99/my-python-app2 .'
            }
        }
        stage('Login to Docker Hub') {
            steps {
                withCredentials([string(credentialsId: 'dockerpass', variable: 'dockerpass')]) {
                    script {
                        bat "docker login -u nadeejachathuranga99 -p %dockerpass%"
                    }
                }
            }
        }
        stage('Push Image') {
            steps {
                bat 'docker push nadeejachathuranga99/my-python-app2'
            }
        }
        stage('Deploy to Minikube') {
            steps {
                script {
                    withCredentials([file(credentialsId: 'k8sconfigpss', variable: 'KUBECONFIG')]) {
                        bat '''
                        kubectl apply -f blue-deployment.yaml
                        kubectl apply -f green-deployment.yaml
                        kubectl apply -f service.yaml
                        kubectl apply -f service-selector.yaml
                        '''
                    }
                }
            }
        }
    }
    post {
        always {
            bat 'docker logout'
        }
    }
}
