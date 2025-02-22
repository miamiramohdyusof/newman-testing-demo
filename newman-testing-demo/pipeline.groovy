pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                git 'https://bitbucket.intranet.rhbgroup.com/scm/ims/newman-testing-demo.git'
            }
        }
        stage('Run API Tests') {
            steps {
                sh '''
                python3 api_test.py FlashRegression SIT
                '''
            }
        }
        stage('Publish Reports') {
            steps {
                publishHTML (target: [
                    reportDir: 'reports/FlashRegression',
                    reportFiles: 'report.html',
                    reportName: 'Newman API Test Report'
                ])
            }
        }
    }
}
