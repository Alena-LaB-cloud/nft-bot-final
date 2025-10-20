import os
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello World from Flask!"

@app.route('/health')
def health():
    return "OK"

port = int(os.environ.get("PORT", 10000))
if __name__ == "__main__":
    print(f"Starting server on port {port}")
    app.run(host="0.0.0.0", port=port)
    logger.info(f"🚀 Starting web server on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
    

