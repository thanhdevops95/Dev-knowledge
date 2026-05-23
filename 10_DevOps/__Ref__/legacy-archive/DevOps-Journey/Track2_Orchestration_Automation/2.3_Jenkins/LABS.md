# 🔬 Labs: Jenkins

> **Hands-on Labs for Jenkins Pipelines**
>
> *Bài thực hành Jenkins Pipelines.*
>
> 💡 Note: GitLab CI is the primary CI/CD platform. Jenkins is taught as an enterprise alternative.
>
> *Lưu ý: GitLab CI là nền tảng CI/CD chính. Jenkins được dạy như một giải pháp thay thế cho doanh nghiệp.*

---

## 🔬 Lab 1: Jenkins Setup

```bash
# Run Jenkins with Docker
docker run -d -p 8080:8080 -p 50000:50000 \
  -v jenkins_home:/var/jenkins_home \
  -v /var/run/docker.sock:/var/run/docker.sock \
  --name jenkins \
  jenkins/jenkins:lts

# Get initial password
docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword

# Access: http://localhost:8080
```

---

## 🔬 Lab 2: First Pipeline

```groovy
// Jenkinsfile
pipeline {
    agent any
    stages {
        stage('Hello') {
            steps {
                echo 'Hello, Jenkins!'
            }
        }
    }
}
```

---

## 🔬 Lab 3: Build and Test

```groovy
pipeline {
    agent any
    
    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/user/repo.git'
            }
        }
        
        stage('Build') {
            steps {
                sh 'npm install'
            }
        }
        
        stage('Test') {
            steps {
                sh 'npm test'
            }
            post {
                always {
                    junit 'test-results/*.xml'
                }
            }
        }
    }
}
```

---

## 🔬 Lab 4: Docker Pipeline

```groovy
pipeline {
    agent {
        docker { image 'node:18-alpine' }
    }
    
    stages {
        stage('Build') {
            steps {
                sh 'node --version'
                sh 'npm install'
            }
        }
    }
}
```

---

## 🔬 Lab 5: Multi-branch Pipeline

```groovy
pipeline {
    agent any
    
    stages {
        stage('Build') {
            steps {
                sh 'make build'
            }
        }
        
        stage('Deploy Staging') {
            when {
                branch 'develop'
            }
            steps {
                sh 'make deploy-staging'
            }
        }
        
        stage('Deploy Production') {
            when {
                branch 'main'
            }
            steps {
                sh 'make deploy-production'
            }
        }
    }
}
```

---

## ✅ Checklist

- [ ] Lab 1: Jenkins Setup (Cài đặt Jenkins)
- [ ] Lab 2: First Pipeline (Pipeline đầu tiên)
- [ ] Lab 3: Build and Test (Build và Test)
- [ ] Lab 4: Docker Pipeline (Pipeline với Docker)
- [ ] Lab 5: Multi-branch (Đa nhánh)

---

**[← Back to README](./README.md)**
