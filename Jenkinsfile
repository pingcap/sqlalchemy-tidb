#!groovy

node('node') {
    agent {
        docker { image 'hawkingrei:14-alpine' }
    }

    currentBuild.result = "SUCCESS"

    try {

       stage('Checkout'){

          
       }

       stage('Linter'){
           agent {
                docker {
                    image 'hawkingrei/django_tidb_test_env:20210819'
        
                    reuseNode true
                }
            }
            checkout scm
            sh 'tox -e lint'

       }

       stage('Build Docker'){

            sh './dockerBuild.sh'
       }

       stage('Deploy'){

         echo 'Push to Repo'
         sh './dockerPushToRepo.sh'

         echo 'ssh to web server and tell it to pull new image'
         sh 'ssh deploy@xxxxx.xxxxx.com running/xxxxxxx/dockerRun.sh'

       }

       stage('Cleanup'){

         echo 'prune and cleanup'
         sh 'npm prune'
         sh 'rm node_modules -rf'

         mail body: 'project build successful',
                     from: 'xxxx@yyyyy.com',
                     replyTo: 'xxxx@yyyy.com',
                     subject: 'project build successful',
                     to: 'yyyyy@yyyy.com'
       }



    }
    catch (err) {

        currentBuild.result = "FAILURE"

            mail body: "project build error is here: ${env.BUILD_URL}" ,
            from: 'xxxx@yyyy.com',
            replyTo: 'yyyy@yyyy.com',
            subject: 'project build failed',
            to: 'zzzz@yyyyy.com'

        throw err
    }

}