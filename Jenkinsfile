pipeline {
    agent any
    
    environment {
        HAPPY_CAT = 'cat #1'
    }

    stages {
        
        
        stage('Checkout') {
            steps {
                echo "Done as part of setting up jenkins"
            }
        }
        stage('Build') {
            steps {
                git branch: 'main', credentialsId: '1a7f5656-8ced-46b4-a61c-0950fbf687c0', url: 'https://github.com/rykng/GundamProject.git'
                echo 'Activate venv from local'
                sh '''source /Users/rng/.virtualenvs/GundamProject/bin/activate'''
                sh '''pip install -r requirements.txt'''
                echo 'Run unittest'
                sh '''pytest --junit-xml=report.xml'''
                junit 'report.xml'
            }
        
        }
        stage('View Envs') {
            steps {
                echo "See View Envs" 
                sh '''env | sort'''
            }
        }
        stage('Deploy') {
            steps {
                echo "Deploying ${ currentBuild.changeSets }  to dev"
            }
        }
        stage('e2e Test') {
            steps {
                echo "Going to run e2e Test vs ${ env.GIT_COMMIT } ${env.BUILD_NUMBER}"
                build 'mathhero'
            }
        }
        stage('GateKeeper') {
            steps {
                echo 'GateKeeper to check if other services pass e2e test'
                echo 'currentBuild.id? -> ${currentBuild.id}'
                echo 'prev success? -> ${currentBuild.previousSuccessfulBuild}'
                echo 'prev fail? -> ${currentBuild.previousFailedBuild}'
                echo 'job URL -> ${env.JOB_URL}'
                echo 'build URL -> ${env.BUILD_URL}'
            }
        }
        stage('Deploy to QA') {
            steps {
                echo "Deploying [ ${ env.GIT_COMMIT } ]to QA vs ${env.JOB_NAME}"
                sh '''env | sort'''
                sh '''deactivate'''
            }
        }
        
    }
}
