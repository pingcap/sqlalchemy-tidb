#!groovy

podTemplate(name: label, label: label, instanceCap: 5,
                workspaceVolume: emptyDirWorkspaceVolume(memory: true),
                nodeSelector: 'role_type=slave',
                containers: [
                        containerTemplate(name: 'dockerd', image: 'docker:18.09.6-dind', privileged: true),
                        containerTemplate(name: 'docker', image: 'hub.pingcap.net/zyguan/docker:build-essential',
                                alwaysPullImage: true, envVars: [
                                envVar(key: 'DOCKER_HOST', value: 'tcp://localhost:2375'),
                        ], ttyEnabled: true, command: 'cat'),
                        containerTemplate(name: 'builder', image: 'hub.pingcap.net/tiflash/tiflash-builder-ci',
                                alwaysPullImage: true, ttyEnabled: true, command: 'cat',
                                resourceRequestCpu: '4000m', resourceRequestMemory: '8Gi',
                                resourceLimitCpu: '10000m', resourceLimitMemory: '30Gi'),
                ]) {
        node(label) {
            currentBuild.result = "SUCCESS"

            try {
                stage('Linter'){
                    checkout scm
                    docker.image('hawkingrei/django_tidb_test_env:20210819').inside {
                    sh 'make test'
                }
            }    
        } catch (err) {
            currentBuild.result = "FAILURE"
            throw err
        }
    }
}