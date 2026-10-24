from flask import Flask

app = Flask(__name__)


@app.route("/")
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Student Information App</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                text-align: center;
                background-color: #f0f4f8;
                padding: 50px;
            }
            .card {
                background: white;
                padding: 30px;
                border-radius: 12px;
                max-width: 500px;
                margin: auto;
                box-shadow: 0 4px 10px rgba(0,0,0,0.1);
            }
            h1 {
                color: #2563eb;
            }
        </style>
    </head>
    <body>
        <div class="card">
            <h1>Student Information App</h1>
            <h2>Welcome!</h2>
            <p><strong>Project:</strong> Docker and Kubernetes Deployment</p>
            <p><strong>Application:</strong> Python Flask</p>
            <p><strong>Status:</strong> Application is running successfully!</p>
        </div>
    </body>
    </html>
    """


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)