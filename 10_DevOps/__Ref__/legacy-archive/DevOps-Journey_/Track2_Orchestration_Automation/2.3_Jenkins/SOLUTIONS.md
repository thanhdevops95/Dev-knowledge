# ✅ Solutions: Jenkins

---

## Exercise 3: Parameterized Build

```groovy
pipeline {
    agent any
    
    parameters {
        string(name: 'VERSION', defaultValue: '1.0.0', description: 'Version to deploy')
        choice(name: 'ENVIRONMENT', choices: ['dev', 'staging', 'production'], description: 'Target environment')
        booleanParam(name: 'RUN_TESTS', defaultValue: true, description: 'Run tests?')
    }
    
    stages {
        stage('Build') {
            steps {
                echo "Building version ${params.VERSION}"
                sh "docker build -t myapp:${params.VERSION} ."
            }
        }
        
        stage('Test') {
            when {
                expression { params.RUN_TESTS }
            }
            steps {
                sh 'npm test'
            }
        }
        
        stage('Deploy') {
            steps {
                echo "Deploying ${params.VERSION} to ${params.ENVIRONMENT}"
            }
        }
    }
}
```

---

## Exercise 4: Parallel Stages

```groovy
pipeline {
    agent any
    
    stages {
        stage('Tests') {
            parallel {
                stage('Unit Tests') {
                    steps {
                        sh 'npm run test:unit'
                    }
                }
                stage('Integration Tests') {
                    steps {
                        sh 'npm run test:integration'
                    }
                }
                stage('E2E Tests') {
                    steps {
                        sh 'npm run test:e2e'
                    }
                }
            }
        }
    }
}
```

---

**[← Back to Exercises](./EXERCISES.md)**
