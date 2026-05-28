# 📋 Jenkins - Cheatsheet

> **Quick Reference for Jenkins Pipelines**
>
> *Tra cứu nhanh Jenkins Pipelines*

> 💡 **Note:** GitLab CI is the primary CI/CD platform for this course. Jenkins is taught as an enterprise alternative.
>
> *GitLab CI là nền tảng CI/CD chính. Jenkins được dạy như một lựa chọn thay thế doanh nghiệp.*

---

## 📝 Declarative Pipeline

```groovy
pipeline {
    agent any
    
    environment {
        REGISTRY = 'registry.example.com'
    }
    
    stages {
        stage('Build') {
            steps {
                sh 'npm install'
                sh 'npm run build'
            }
        }
        
        stage('Test') {
            steps {
                sh 'npm test'
            }
        }
        
        stage('Deploy') {
            when {
                branch 'main'
            }
            steps {
                sh 'docker build -t $REGISTRY/app .'
                sh 'docker push $REGISTRY/app'
            }
        }
    }
    
    post {
        always {
            cleanWs()
        }
        success {
            echo 'Pipeline succeeded!'
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
}
```

---

## 🔧 Common Steps (Các bước thường dùng)

```groovy
// Shell command (Lệnh shell)
sh 'npm install'

// Windows command (Lệnh Windows)
bat 'npm install'

// Checkout code (Lấy code)
checkout scm

// Archive artifacts (Lưu artifacts)
archiveArtifacts artifacts: 'dist/**/*'

// Publish test results (Xuất kết quả test)
junit 'test-results/*.xml'

// Environment variables (Biến môi trường)
withEnv(['NODE_ENV=production']) {
    sh 'npm run build'
}

// Credentials (Thông tin xác thực)
withCredentials([usernamePassword(credentialsId: 'docker-hub', 
    usernameVariable: 'USER', passwordVariable: 'PASS')]) {
    sh 'docker login -u $USER -p $PASS'
}
```

---

## 🔄 Jenkins vs GitLab CI (So sánh)

| Feature | Jenkins | GitLab CI |
|---------|---------|-----------|
| Config file | `Jenkinsfile` | `.gitlab-ci.yml` |
| Syntax | Groovy | YAML |
| Hosting | Self-hosted (Tự host) | SaaS or Self-hosted (SaaS hoặc Tự host) |
| Docker | Plugin required (Cần Plugin) | Built-in (Tích hợp sẵn) |

---

## 🔗 Navigation

| ← Previous | Current | Next → |
|------------|---------|--------|
| [README](./README.md) | **Cheatsheet** | [LABS](./LABS.md) |

---

*Last Updated: 2025-12-30*
