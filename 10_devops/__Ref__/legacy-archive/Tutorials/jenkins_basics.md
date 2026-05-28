# Hướng dẫn Jenkins

<u>Version:</u> 1.0.0  
<u>Author:</u> ThanhRòm  
<u>Release Date:</u> 2025-12-17

## 📋**GIỚI THIỆU**

Jenkins là công cụ CI/CD mã nguồn mở phổ biến nhất, giúp tự động hóa việc build, test và deploy.

---

## 🔧**CÀI ĐẶT**

### Docker (Khuyên dùng)

```bash
docker run -d \
  --name jenkins \
  -p 8080:8080 \
  -p 50000:50000 \
  -v jenkins_home:/var/jenkins_home \
  jenkins/jenkins:lts
```

### Ubuntu/Debian

```bash
# Thêm key và repo
curl -fsSL https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key | sudo tee \
  /usr/share/keyrings/jenkins-keyring.asc > /dev/null

echo deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc] \
  https://pkg.jenkins.io/debian-stable binary/ | sudo tee \
  /etc/apt/sources.list.d/jenkins.list > /dev/null

# Cài đặt
sudo apt update
sudo apt install jenkins

# Khởi động
sudo systemctl start jenkins
sudo systemctl enable jenkins
```

### Lấy password ban đầu

```bash
# Docker
docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword

# Linux
sudo cat /var/lib/jenkins/secrets/initialAdminPassword
```

### Truy cập

```
http://localhost:8080
```

---

## 📦**PLUGINS CẦN THIẾT**

### Cài đặt Plugins

1. **Manage Jenkins** → **Manage Plugins**
2. Tab **Available** → Tìm và cài:

| Plugin | Mô tả |
|--------|-------|
| **Pipeline** | Jenkinsfile support |
| **Git** | Git integration |
| **GitHub** | GitHub webhooks |
| **Blue Ocean** | Modern UI |
| **Docker Pipeline** | Docker support |
| **Credentials** | Manage credentials |
| **SSH Agent** | SSH keys |
| **Slack Notification** | Slack alerts |

---

## 🔄**FREESTYLE JOB**

### Tạo Freestyle Job

1. **New Item** → Nhập tên → **Freestyle project**
2. Cấu hình:
   - **Source Code Management**: Git URL
   - **Build Triggers**: Poll SCM, GitHub webhook
   - **Build Steps**: Execute shell
   - **Post-build Actions**: Archive, Email, Slack

### Build Steps (Shell)

```bash
# Install dependencies
pip install -r requirements.txt

# Run tests
pytest

# Build
python setup.py build
```

---

## 📝**JENKINS PIPELINE**

### Jenkinsfile cơ bản

```groovy
// Jenkinsfile
pipeline {
    agent any
    
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/user/repo.git'
            }
        }
        
        stage('Build') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }
        
        stage('Test') {
            steps {
                sh 'pytest --junitxml=reports/test-results.xml'
            }
            post {
                always {
                    junit 'reports/test-results.xml'
                }
            }
        }
        
        stage('Deploy') {
            when {
                branch 'main'
            }
            steps {
                sh './deploy.sh'
            }
        }
    }
    
    post {
        success {
            echo 'Build succeeded!'
        }
        failure {
            echo 'Build failed!'
        }
        always {
            cleanWs()
        }
    }
}
```

### Pipeline với Docker

```groovy
pipeline {
    agent {
        docker {
            image 'python:3.11'
            args '-v $HOME/.cache/pip:/root/.cache/pip'
        }
    }
    
    stages {
        stage('Test') {
            steps {
                sh 'pip install -r requirements.txt'
                sh 'pytest'
            }
        }
    }
}
```

### Multi-stage Pipeline

```groovy
pipeline {
    agent none
    
    stages {
        stage('Build') {
            agent {
                docker { image 'node:18' }
            }
            steps {
                sh 'npm install'
                sh 'npm run build'
                stash includes: 'dist/**', name: 'build'
            }
        }
        
        stage('Test') {
            agent {
                docker { image 'node:18' }
            }
            steps {
                sh 'npm test'
            }
        }
        
        stage('Deploy') {
            agent any
            steps {
                unstash 'build'
                sh './deploy.sh'
            }
        }
    }
}
```

---

## 🔐**CREDENTIALS**

### Thêm Credentials

1. **Manage Jenkins** → **Manage Credentials**
2. **Global** → **Add Credentials**
3. Chọn loại:
   - Username with password
   - SSH Username with private key
   - Secret text
   - Secret file

### Sử dụng trong Pipeline

```groovy
pipeline {
    agent any
    
    environment {
        DOCKER_CREDS = credentials('docker-hub-creds')
        AWS_ACCESS_KEY = credentials('aws-access-key')
    }
    
    stages {
        stage('Deploy') {
            steps {
                // Username/Password
                withCredentials([usernamePassword(
                    credentialsId: 'docker-hub-creds',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh 'docker login -u $DOCKER_USER -p $DOCKER_PASS'
                }
                
                // SSH Key
                withCredentials([sshUserPrivateKey(
                    credentialsId: 'ssh-key',
                    keyFileVariable: 'SSH_KEY'
                )]) {
                    sh 'ssh -i $SSH_KEY user@server'
                }
            }
        }
    }
}
```

---

## 🔔**NOTIFICATIONS**

### Email

```groovy
post {
    failure {
        mail to: 'team@example.com',
             subject: "Failed: ${currentBuild.fullDisplayName}",
             body: "Build failed: ${env.BUILD_URL}"
    }
}
```

### Slack

```groovy
post {
    success {
        slackSend channel: '#builds',
                  color: 'good',
                  message: "Build succeeded: ${env.JOB_NAME} ${env.BUILD_NUMBER}"
    }
    failure {
        slackSend channel: '#builds',
                  color: 'danger',
                  message: "Build failed: ${env.JOB_NAME} ${env.BUILD_NUMBER}"
    }
}
```

---

## 📊**ENVIRONMENT & PARAMETERS**

### Environment Variables

```groovy
pipeline {
    agent any
    
    environment {
        APP_NAME = 'my-app'
        VERSION = '1.0.0'
        DEPLOY_ENV = "${env.BRANCH_NAME == 'main' ? 'production' : 'staging'}"
    }
    
    stages {
        stage('Build') {
            steps {
                sh 'echo "Building $APP_NAME v$VERSION for $DEPLOY_ENV"'
            }
        }
    }
}
```

### Parameters

```groovy
pipeline {
    agent any
    
    parameters {
        string(name: 'VERSION', defaultValue: '1.0.0', description: 'Version to deploy')
        choice(name: 'ENVIRONMENT', choices: ['dev', 'staging', 'production'], description: 'Target environment')
        booleanParam(name: 'RUN_TESTS', defaultValue: true, description: 'Run tests?')
    }
    
    stages {
        stage('Deploy') {
            when {
                expression { params.RUN_TESTS == true }
            }
            steps {
                sh "deploy.sh ${params.VERSION} ${params.ENVIRONMENT}"
            }
        }
    }
}
```

---

## 🌿**MULTIBRANCH PIPELINE**

### Cấu hình

1. **New Item** → **Multibranch Pipeline**
2. **Branch Sources** → **Git** → URL
3. Jenkins tự động tạo job cho mỗi branch có Jenkinsfile

### Jenkinsfile cho Multibranch

```groovy
pipeline {
    agent any
    
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
        
        stage('Deploy to Staging') {
            when {
                branch 'develop'
            }
            steps {
                sh './deploy.sh staging'
            }
        }
        
        stage('Deploy to Production') {
            when {
                branch 'main'
            }
            steps {
                input message: 'Deploy to production?'
                sh './deploy.sh production'
            }
        }
    }
}
```

---

## 🐳**DOCKER BUILD & PUSH**

```groovy
pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE = 'username/my-app'
        DOCKER_TAG = "${env.BUILD_NUMBER}"
    }
    
    stages {
        stage('Build Docker Image') {
            steps {
                sh "docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} ."
                sh "docker tag ${DOCKER_IMAGE}:${DOCKER_TAG} ${DOCKER_IMAGE}:latest"
            }
        }
        
        stage('Push to Registry') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'docker-hub',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh 'echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin'
                    sh "docker push ${DOCKER_IMAGE}:${DOCKER_TAG}"
                    sh "docker push ${DOCKER_IMAGE}:latest"
                }
            }
        }
    }
    
    post {
        always {
            sh "docker rmi ${DOCKER_IMAGE}:${DOCKER_TAG} || true"
        }
    }
}
```

---

## 📁**SHARED LIBRARIES**

### Cấu trúc

```
vars/
├── buildPython.groovy
└── deployToServer.groovy
src/
└── org/myorg/
    └── Utils.groovy
```

### vars/buildPython.groovy

```groovy
def call(Map config = [:]) {
    pipeline {
        agent any
        
        stages {
            stage('Install') {
                steps {
                    sh 'pip install -r requirements.txt'
                }
            }
            stage('Test') {
                steps {
                    sh 'pytest'
                }
            }
        }
    }
}
```

### Sử dụng

```groovy
@Library('my-shared-library') _

buildPython()
```

---

## **LIÊN HỆ**

*Made with ❤️ by ThanhRòm*
