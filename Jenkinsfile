pipeline {
    agent any

    environment {
        REGISTRY = 'registry.spearmanwm.dev'
        IMAGE_NAME = 'url_processor'
        HOME = '${WORKSPACE}'
    }

    stages {
        stage('clone') {
            steps {
                git branch: 'main', credentialsId: 'GitHubCredentials', url: 'https://github.com/WilliamSpear1/Downloader.git'
            }
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
                    def dockerImage = docker.build("${REGISTRY}/${IMAGE_NAME}:latest")
                }
            }
        }

        stage('push to private registry') {
            steps {
                script {
                   docker.withRegistry("${REGISTRY}") {
                        dockerImage.push()
                    }
                }
            }
        }
    }
}
post {
    always {
        cleanWs()
    }
}