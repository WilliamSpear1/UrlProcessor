def dockerImage
pipeline {
    agent any
    
    options {
        skipDefaultCheckout() // Prevent Jenkins from auto-checking out with tag attempt
    }
    
    environment {
        REGISTRY = 'registry.spearmanwm.dev'
        IMAGE_NAME = 'url_processor'
        HOME = '${WORKSPACE}'
    }

    stages {
        stage('clone') {
            steps {
                checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'GitHubCredentials', url: 'https://github.com/WilliamSpear1/UrlProcessor.git']])
        }

        stage('setup git config') {
            steps {
                sh '''
                    git config user.name "William Spearman"
                    git config user.email "wspearman.protonmail.com"
                '''
            }
        }

        stage('build docker image') {
            steps {
                script {
                    dockerImage = docker.build("${REGISTRY}/${IMAGE_NAME}:latest")
                }
            }
        }

        stage('push to private registry') {
            steps {
                script {
                   docker.withRegistry("https://registry.spearmanwm.dev") {
                        dockerImage.push()
                    }
                }
            }
        }
    }
    post {
        always {
            script{
                cleanWs()
            }
        }
    }
}