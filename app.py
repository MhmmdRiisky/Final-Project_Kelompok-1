from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "🚀 Hello from Flask App on Kubernetes with Jenkins! INI KELOMPOK-1"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
