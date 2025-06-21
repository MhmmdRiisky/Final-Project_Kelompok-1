pipeline {
  agent any

  environment {
    IMAGE = "user/demo-app" 
    TAG = "latest"
    REGISTRY = "docker.io"
    DOCKER_CRED = "docker-hub"
    NAMESPACE = "default"
  }

  stages {
    stage('Checkout Source Code') {
      steps {
        git url: 'https://github.com/MhmmdRiisky/Final-Project_Kelompok-1.git', branch: 'main'
      }
    }

    stage('Build Docker Image') {
      steps {
        script {
          echo "🛠️ Building image ${IMAGE}:${TAG}..."
          def builtImage = docker.build("${IMAGE}:${TAG}")
        }
      }
    }

    stage('Push Docker Image to Local Registry') {
      steps {
        withCredentials([usernamePassword(
          credentialsId: "docker-hub",
          usernameVariable: 'USER',
          passwordVariable: 'PASS'
        )]) {
          script {
            echo "📦 Pushing image to local Docker registry..."
            sh """
              echo "$PASS" | docker login -u "$USER" --password-stdin
              docker tag ${IMAGE}:${TAG} ${REGISTRY}/${IMAGE}:${TAG}
              docker push ${REGISTRY}/${IMAGE}:${TAG}
            """
          }
        }
      }
    }

    stage('Deploy to Kubernetes') {
      steps {
        script {
          echo "🚀 Deploying to Kubernetes using kubectl apply..."
          sh '''
            export KUBECONFIG=/var/jenkins_home/kubeconfig
            kubectl apply -f deployment.yaml
          '''
        }
      }
    }
  }

  post {
    success {
      echo "✅ Pipeline Sukses: Aplikasi berhasil dideploy ke Kubernetes"
    }
    failure {
      echo "❌ Pipeline Gagal: Cek log untuk mengetahui error"
    }
  }
}
