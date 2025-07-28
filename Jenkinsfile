pipeline {
    agent any

    environment {
        REGISTRY = 'registry.spearmanwm.dev'
        IMAGE_NAME = '${REGISTRY}/url_processor'
    }

    stages {
        stage('clone') {
            steps {
                git url: 'https://github.com/WilliamSpear1/URlProcessor.git', branch:'main'
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
                    docker.build("${IMAGE_NAME}:latest")
                }
            }
        }

        stage('push to private registry') {
            steps {
                scripts {
                    sh """
                     echo docker push ${IMAGE_NAME}:latest
                    """
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
