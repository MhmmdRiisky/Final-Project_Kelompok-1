pipeline {
  agent any

  environment {
    IMAGE = "user/demo-app"
    TAG = "latest"
    REGISTRY = "192.168.49.4:5000"
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
          docker.build("${IMAGE}:${TAG}", "--no-cache")
        }
      }
    }

    stage('Push Docker Image to Local Registry') {
      steps {
        script {
          echo "📦 Pushing image to local Docker registry..."
          sh """
            docker tag ${IMAGE}:${TAG} ${REGISTRY}/${IMAGE}:${TAG}
            docker push ${REGISTRY}/${IMAGE}:${TAG}
          """
        }
      }
    }

    stage('Deploy to Kubernetes') {
      steps {
        script {
          echo "🚀 Deploying to Kubernetes using kubectl apply..."
          withEnv(["KUBECONFIG=/kubeconfig"]) {
            sh """
                # GANTI placeholder di YAML dengan nama image yang BENAR
                sed -i 's|IMAGE_PLACEHOLDER|${REGISTRY}/${IMAGE}:${TAG}|g' deployment.yaml
                
                # Terapkan YAML yang sudah diupdate
                kubectl apply -f deployment.yaml
                kubectl apply -f service.yaml
            """
          }
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

