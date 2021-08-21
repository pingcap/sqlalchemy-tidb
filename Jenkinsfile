#!groovy

node {
    agent {
        docker { image 'hawkingrei:14-alpine' }
    }

    currentBuild.result = "SUCCESS"

    try {
       stage('Linter'){
            checkout scm
            docker.image('hawkingrei/django_tidb_test_env:20210819').inside {
                sh 'make test'
            }
       }
    }
    catch (err) {

        currentBuild.result = "FAILURE"
        throw err
    }

}